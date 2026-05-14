#!/usr/bin/env python3
"""
automated_lab/engine/scheduler.py
==================================
Orquestador nocturno para protein-lab.

Diseño v2:
- Respeta max_experiments/time_budget_minutes del campaign brief.
- IDs estables y únicos: no pisa archivos de resultados.
- Integra KISS/LLM en idea_generation si hay provider cloud disponible.
- Genera reporte matutino con resumen mecánico + revisión del investigador cloud.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

LAB_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(LAB_DIR / "automated_lab"))

DEFAULT_BATCH_SIZE = 50
DEFAULT_EXPERIMENTS_PER_HOUR = 500
RESULTS_DIR = LAB_DIR / "automated_lab" / "results"
CAMPAIGNS_DIR = LAB_DIR / "automated_lab" / "campaign_briefs"


class Scheduler:
    """Orquestador del automated lab loop."""

    def __init__(self, *, batch_size: int = DEFAULT_BATCH_SIZE):
        self.runner = None
        self.ideas: list[dict[str, Any]] = []
        self.batch_size = batch_size
        self.campaign: dict[str, Any] = {}

    def _load_runner(self):
        if self.runner is None:
            from engine.experiment import ExperimentRunner
            self.runner = ExperimentRunner()

    def load_campaign(self, campaign_name: str) -> dict[str, Any]:
        brief_file = CAMPAIGNS_DIR / f"{campaign_name}.json"
        if not brief_file.exists():
            brief_file = CAMPAIGNS_DIR / f"{campaign_name}.md"
            if not brief_file.exists():
                raise FileNotFoundError(f"Campaign not found: {campaign_name}")
        content = brief_file.read_text()
        if brief_file.suffix == ".json":
            campaign = json.loads(content)
        else:
            campaign = {"campaign": campaign_name, "brief_md": content, "experiments": []}
        campaign.setdefault("campaign", campaign_name)
        self.campaign = campaign
        return campaign

    def generate_experiments(self, campaign: dict[str, Any], *, count: int | None = None) -> list[dict[str, Any]]:
        max_count = count or int(campaign.get("max_experiments", self.batch_size))
        if campaign.get("experiments"):
            experiments = campaign["experiments"][:max_count]
        else:
            from idea_generation.generator import IdeaGenerator
            gen = IdeaGenerator()
            self.ideas = gen.generate(
                campaign.get("campaign", "default"),
                campaign.get("brief_md", ""),
                count=max_count,
                campaign=campaign,
            )
            experiments = [self._idea_to_experiment(idea) for idea in self.ideas]
        return self._dedupe_experiments(experiments)[:max_count]

    def _idea_to_experiment(self, idea: dict[str, Any]) -> dict[str, Any]:
        exp = {
            "id": idea.get("id"),
            "type": idea.get("type", "dti_pkd"),
            "target": idea.get("target", ""),
            "target_seq": idea.get("target_seq", ""),
            "drug_name": idea.get("drug_name", ""),
            "drug_smiles": idea.get("drug_smiles", ""),
            "campaign": idea.get("campaign", "default"),
            "hypothesis": idea.get("hypothesis", ""),
            "rationale": idea.get("rationale", ""),
            "priority_score": idea.get("priority_score"),
            "source": idea.get("source", "unknown"),
            "params": idea.get("params", {}),
        }
        if not exp["id"]:
            from idea_generation.generator import IdeaGenerator
            exp["id"] = IdeaGenerator.stable_id(exp)
        return exp

    @staticmethod
    def _dedupe_experiments(experiments: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: set[tuple[str, str, str]] = set()
        out = []
        for exp in experiments:
            key = (exp.get("type", ""), exp.get("drug_name", ""), exp.get("target", ""))
            if key in seen:
                continue
            seen.add(key)
            out.append(exp)
        return out

    def run_campaign(self, campaign_name: str, *, hours: float | None = None,
                     max_experiments: int | None = None) -> list[dict[str, Any]]:
        self._load_runner()
        campaign = self.load_campaign(campaign_name)

        time_budget_minutes = campaign.get("time_budget_minutes")
        if hours is None:
            # CLI default is one-shot. Night autonomy must be explicit via
            # scripts/run_overnight.sh or --overnight N; otherwise a harmless
            # smoke command would unexpectedly run for hours.
            hours = 0.0

        if max_experiments is None:
            if hours and hours > 0:
                default_max = max(1, int(hours * DEFAULT_EXPERIMENTS_PER_HOUR))
                max_experiments = int(campaign.get("max_experiments", default_max))
            else:
                max_experiments = min(self.batch_size, int(campaign.get("max_experiments", self.batch_size)))

        print(f"\n{'='*70}")
        print("AUTOMATED LAB — CAMPAÑA" + (" NOCTURNA" if hours and hours > 0 else " ONE-SHOT"))
        print(f"  Campaña: {campaign_name}")
        print(f"  Modelo investigador: {self._provider_label()}")
        print(f"  Presupuesto: {hours or 0:.3f}h | máximo {max_experiments} experimentos")
        print(f'  Inicio: {datetime.now().strftime("%Y-%m-%d %H:%M")}' )
        print(f"{'='*70}\n")

        experiments = self.generate_experiments(campaign, count=max_experiments)
        print(f"[scheduler] {len(experiments)} experimentos generados")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = RESULTS_DIR / f"{campaign_name}_{timestamp}"
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "EXPERIMENT_QUEUE.json").write_text(json.dumps(experiments, indent=2, ensure_ascii=False))

        all_results: list[dict[str, Any]] = []
        t_start = time.time()
        t_end = t_start + ((hours or 0) * 3600)
        cycle = 0
        idx = 0
        while idx < len(experiments):
            if hours and hours > 0 and time.time() >= t_end:
                print("[scheduler] Presupuesto de tiempo agotado")
                break
            cycle += 1
            batch = experiments[idx: idx + self.batch_size]
            idx += len(batch)
            cycle_dir = run_dir / f"cycle_{cycle:03d}"
            cycle_dir.mkdir(exist_ok=True)
            print(f"\n[scheduler] Ciclo {cycle} — {len(batch)} experimentos")
            assert self.runner is not None
            results = self.runner.run_batch(batch, results_dir=cycle_dir, sequential=False)
            all_results.extend(results)
            ok = sum(1 for r in results if r.get("status") == "ok")
            err = sum(1 for r in results if r.get("status") == "error")
            print(f"[scheduler]   ✅ {ok} OK | ❌ {err} ERROR | Total: {len(all_results)}/{len(experiments)}")
            if not hours or hours <= 0:
                break

        report = self._generate_report(campaign_name, all_results, t_start, campaign)
        report_file = run_dir / "REPORTE_MANANA.md"
        report_file.write_text(report)
        print(f"\n[scheduler] Reporte matutino: {report_file}")

        session = {
            "campaign": campaign_name,
            "provider": self._provider_label(),
            "duration_hours": round((time.time() - t_start) / 3600, 4),
            "cycles": cycle,
            "total_experiments": len(all_results),
            "successful": sum(1 for r in all_results if r.get("status") == "ok"),
            "errors": sum(1 for r in all_results if r.get("status") == "error"),
            "run_dir": str(run_dir),
            "timestamp": datetime.now().isoformat(),
        }
        (run_dir / "SESSION.json").write_text(json.dumps(session, indent=2, ensure_ascii=False))
        print(f"\n{'='*70}")
        print("CAMPAÑA COMPLETADA")
        print(f"  Experimentos: {session['total_experiments']}")
        print(f"  Éxito: {session['successful']}")
        print(f"  Errores: {session['errors']}")
        print(f"  Duración: {session['duration_hours']:.3f}h")
        print(f"  Resultados: {run_dir}")
        print(f"{'='*70}")
        return all_results

    def _provider_label(self) -> str:
        try:
            from llm_researcher import resolve_provider
            provider = resolve_provider()
            return f"{provider.name}/{provider.model}" if provider else "none"
        except Exception:
            return "unavailable"

    def _generate_report(self, campaign_name: str, results: list[dict[str, Any]],
                         t_start: float, campaign: dict[str, Any]) -> str:
        ok = [r for r in results if r.get("status") == "ok"]
        err = [r for r in results if r.get("status") == "error"]
        duration = (time.time() - t_start) / 60
        pkd_results = [r for r in ok if "pkd" in r]
        pkd_results.sort(key=lambda x: x.get("pkd", 0), reverse=True)
        lines = [
            f"# Reporte Automatizado — {campaign_name}",
            f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**Duración:** {duration:.1f} minutos",
            f"**Investigador cloud:** {self._provider_label()}",
            f"**Experimentos:** {len(results)} total, {len(ok)} exitosos, {len(err)} errores",
            "",
            "## Top Binding Affinities (pKd)",
            "",
            "| # | Fármaco | Target | pKd | Kd (M) | Backend |",
            "|---|---------|--------|-----|--------|---------|",
        ]
        for i, r in enumerate(pkd_results[:25], 1):
            kd = r.get("kd_molar", 0)
            lines.append(
                f"| {i} | {r.get('drug_name', '?')} | {r.get('target', '?')} | "
                f"{r.get('pkd', 0):.2f} | {kd:.2e} | {r.get('backend', '?')} |"
            )
        if err:
            lines.extend(["", "## Errores", ""])
            for e in err[:20]:
                lines.append(f"- {e.get('experiment_id', '?')}: {e.get('error', '?')}")
        lines.extend(["", "## Revisión del investigador", ""])
        try:
            from llm_researcher import CloudResearcher
            review = CloudResearcher().summarize_results(campaign, pkd_results)
        except Exception:
            review = None
        lines.append(review or "Investigador cloud no disponible; se conserva reporte mecánico solamente.")
        lines.extend([
            "",
            "## Cautela",
            "- MAMMAL entrega predicciones computacionales de afinidad, no validación clínica.",
            "- No promover targets a Tier 1 sin grounding DOI/PMID/PMC y verificación independiente.",
            "",
            "---",
            "*Generado por Automated Lab v2 | DAVI | KISS + cloud investigator + MAMMAL local*",
        ])
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Automated Lab Scheduler")
    parser.add_argument("--campaign", type=str, default="fibromialgia_ruta_b")
    parser.add_argument("--overnight", type=float, default=None,
                        help="Duración en horas. Si se omite, corre one-shot o time_budget_minutes del brief.")
    parser.add_argument("--hours", type=float, default=None, help="Alias explícito para --overnight")
    parser.add_argument("--max-experiments", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    args = parser.parse_args()

    hours = args.overnight if args.overnight is not None else args.hours
    sched = Scheduler(batch_size=args.batch_size)
    sched.run_campaign(args.campaign, hours=hours, max_experiments=args.max_experiments)


if __name__ == "__main__":
    main()
