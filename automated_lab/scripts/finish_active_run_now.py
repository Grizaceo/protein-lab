#!/usr/bin/env python3
"""Finish the current automated_lab ACTIVE_RUN immediately, without pacing.

This is an operational repair/acceleration script: it preserves the existing run_dir,
reads EXPERIMENT_QUEUE.json, skips already-written experiment IDs, executes only the
remaining items in batches, then writes REPORTE_MANANA.md, SESSION.json, STATUS.json,
and results/ACTIVE_RUN.json as completed.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

LAB_DIR = Path(__file__).resolve().parent.parent.parent
AUTO_DIR = LAB_DIR / "automated_lab"
RESULTS_DIR = AUTO_DIR / "results"
sys.path.insert(0, str(AUTO_DIR))

from engine.experiment import ExperimentRunner  # noqa: E402
from engine.scheduler import Scheduler  # noqa: E402

BATCH_SIZE = int(os.environ.get("FINISH_NOW_BATCH_SIZE", "50"))


def load_existing_results(run_dir: Path) -> tuple[list[dict[str, Any]], set[str]]:
    results: list[dict[str, Any]] = []
    done_ids: set[str] = set()
    files = sorted(run_dir.glob("cycle_*/*.json"))
    for path in files:
        try:
            payload = json.loads(path.read_text())
            exp = payload.get("experiment", {})
            res = payload.get("result", {})
            exp_id = exp.get("id") or res.get("experiment_id") or path.stem
            if exp_id:
                done_ids.add(exp_id)
            # Ensure old result objects have the fields the report expects.
            res.setdefault("experiment_id", exp_id)
            res.setdefault("drug_name", exp.get("drug_name", "?"))
            res.setdefault("target", exp.get("target", "?"))
            results.append(res)
        except Exception as e:
            print(f"[finish-now] ⚠ no pude leer {path}: {e}")
    return results, done_ids


def next_cycle_number(run_dir: Path) -> int:
    nums = []
    for d in run_dir.glob("cycle_*"):
        if d.is_dir():
            try:
                nums.append(int(d.name.split("_")[-1]))
            except ValueError:
                pass
    return (max(nums) + 1) if nums else 1


def write_status(run_dir: Path, campaign_name: str, started_at_epoch: float, budget_hours: float,
                 cycle: int, total_batches: int, results: list[dict[str, Any]], status: str = "running") -> None:
    ok = sum(1 for r in results if r.get("status") == "ok")
    err = sum(1 for r in results if r.get("status") == "error")
    payload = {
        "campaign": campaign_name,
        "run_dir": str(run_dir),
        "provider": Scheduler()._provider_label(),
        "status": status,
        "cycle": cycle,
        "total_batches": total_batches,
        "total_results": len(results),
        "successful": ok,
        "errors": err,
        "started_at_epoch": started_at_epoch,
        "elapsed_minutes": round((time.time() - started_at_epoch) / 60, 2),
        "budget_hours": budget_hours,
        "updated_at": datetime.now().isoformat(),
    }
    (run_dir / "STATUS.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    (RESULTS_DIR / "ACTIVE_RUN.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> int:
    active_path = RESULTS_DIR / "ACTIVE_RUN.json"
    if not active_path.exists():
        raise SystemExit("[finish-now] No existe results/ACTIVE_RUN.json")
    active = json.loads(active_path.read_text())
    campaign_name = active.get("campaign", "fibromialgia_ruta_b")
    run_dir = Path(active["run_dir"])
    queue_path = run_dir / "EXPERIMENT_QUEUE.json"
    if not queue_path.exists():
        raise SystemExit(f"[finish-now] No existe cola: {queue_path}")

    queue = json.loads(queue_path.read_text())
    all_results, done_ids = load_existing_results(run_dir)
    remaining = [exp for exp in queue if exp.get("id") not in done_ids]
    started_at_epoch = float(active.get("started_at_epoch") or time.time())
    budget_hours = float(active.get("budget_hours") or 0)
    total_batches = max(1, (len(queue) + BATCH_SIZE - 1) // BATCH_SIZE)
    cycle = next_cycle_number(run_dir) - 1

    print("=" * 70)
    print("AUTOMATED LAB — FINISH NOW")
    print(f"  Campaña: {campaign_name}")
    print(f"  Run dir: {run_dir}")
    print(f"  Cola: {len(queue)} | ya hechos: {len(done_ids)} | restantes: {len(remaining)}")
    print(f"  Batch size: {BATCH_SIZE}")
    print("=" * 70)

    runner = ExperimentRunner()
    for offset in range(0, len(remaining), BATCH_SIZE):
        batch = remaining[offset: offset + BATCH_SIZE]
        cycle += 1
        cycle_dir = run_dir / f"cycle_{cycle:03d}"
        cycle_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n[finish-now] Ciclo {cycle} — {len(batch)} experimentos restantes")
        results = runner.run_batch(batch, results_dir=cycle_dir, sequential=False)
        all_results.extend(results)
        ok = sum(1 for r in results if r.get("status") == "ok")
        err = sum(1 for r in results if r.get("status") == "error")
        print(f"[finish-now]   ✅ {ok} OK | ❌ {err} ERROR | Total: {len(all_results)}/{len(queue)}")
        write_status(run_dir, campaign_name, started_at_epoch, budget_hours, cycle, total_batches, all_results)

    scheduler = Scheduler(batch_size=BATCH_SIZE)
    campaign = scheduler.load_campaign(campaign_name)
    report = scheduler._generate_report(campaign_name, all_results, started_at_epoch, campaign)
    report_file = run_dir / "REPORTE_MANANA.md"
    report_file.write_text(report)

    session = {
        "campaign": campaign_name,
        "provider": scheduler._provider_label(),
        "duration_hours": round((time.time() - started_at_epoch) / 3600, 4),
        "cycles": cycle,
        "total_experiments": len(all_results),
        "successful": sum(1 for r in all_results if r.get("status") == "ok"),
        "errors": sum(1 for r in all_results if r.get("status") == "error"),
        "run_dir": str(run_dir),
        "timestamp": datetime.now().isoformat(),
        "finished_by": "scripts/finish_active_run_now.py",
    }
    (run_dir / "SESSION.json").write_text(json.dumps(session, indent=2, ensure_ascii=False))
    final_status = dict(session)
    final_status["status"] = "completed"
    final_status["updated_at"] = datetime.now().isoformat()
    (run_dir / "STATUS.json").write_text(json.dumps(final_status, indent=2, ensure_ascii=False))
    (RESULTS_DIR / "ACTIVE_RUN.json").write_text(json.dumps(final_status, indent=2, ensure_ascii=False))

    print("\n" + "=" * 70)
    print("CAMPAÑA COMPLETADA — FINISH NOW")
    print(f"  Experimentos: {session['total_experiments']}")
    print(f"  Éxito: {session['successful']}")
    print(f"  Errores: {session['errors']}")
    print(f"  Duración total desde inicio: {session['duration_hours']:.3f}h")
    print(f"  Reporte: {report_file}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
