import os
import sys
import yaml
import asyncio
import logging
import time
from pathlib import Path
from datetime import datetime

# Adjust paths to import local packages correctly
BRIDGE_DIR = Path(__file__).resolve().parent
LAB_DIR = BRIDGE_DIR.parent.parent
sys.path.insert(0, str(BRIDGE_DIR))
sys.path.insert(0, str(LAB_DIR))
sys.path.insert(0, str(LAB_DIR / "automated_lab"))

# Ensure agentic-lab-eac is in sys.path
EAC_SRC = Path("/home/gris/.hermes/workspace/agentic-lab-eac/src")
if EAC_SRC.exists() and str(EAC_SRC) not in sys.path:
    sys.path.insert(0, str(EAC_SRC))

from agentic_lab_eac.models import LabState, ResourceState, ExperimentSpec, ExperimentStep
from agentic_lab_eac.eac import load_lab_config, lab_state_from_config

from eac_bridge.ledger import ResearchLedger
from eac_bridge.safety import WSLSafetyMonitor
from eac_bridge.literature import CombinedLiteratureProvider
from eac_bridge.brute_generator import BruteHypothesisGenerator
from eac_bridge.reasoning import LLMReasoningBridge
from eac_bridge.world_model import LocalWorldModel
from eac_bridge.compiler import ProteinLabCompiler
from eac_bridge.executor import ProteinLabExecutor

# Set up logging to stdout & file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(BRIDGE_DIR / "run_eac.log", mode="a")
    ]
)
logger = logging.getLogger("eac_bridge")

async def run_eac_campaign(campaign_name: str, max_experiments: int = 3, hours: float = 0.0):
    t_start = time.time()
    logger.info(f"=== INITIALIZING EAC BRIDGE CAMPAIGN: {campaign_name} ===")

    # Load configuration
    config_path = BRIDGE_DIR / "protein_lab_eac.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # 1. Initialize core managers
    ledger = ResearchLedger()
    safety_monitor = WSLSafetyMonitor(ledger, config)
    literature = CombinedLiteratureProvider()
    brute_gen = BruteHypothesisGenerator()
    reasoning_bridge = LLMReasoningBridge()
    world_model = LocalWorldModel(ledger, config)
    compiler = ProteinLabCompiler()
    executor = ProteinLabExecutor(ledger)

    # 2. Acquire WSL Cron Lock
    logger.info("Checking cron overlap lock...")
    safety_monitor.acquire_lock()

    try:
        # Load target sequences FASTA
        fasta_path = LAB_DIR / "investigacion-fibromialgia" / "datos" / "target_sequences.fasta"
        fasta_sequences = {}
        if fasta_path.exists():
            try:
                current_header = None
                current_seq = []
                with open(fasta_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith(">"):
                            if current_header:
                                fasta_sequences[current_header] = "".join(current_seq)
                            parts = line[1:].split("|")
                            current_header = parts[0].upper()
                            current_seq = []
                        else:
                            current_seq.append(line)
                    if current_header:
                        fasta_sequences[current_header] = "".join(current_seq)
                logger.info(f"Loaded {len(fasta_sequences)} sequences from FASTA.")
            except Exception as e:
                logger.warning(f"Failed to load FASTA: {e}")

        # 3. Running WSL safety audits
        logger.info("Auditing WSL environment...")
        safety_monitor.check_gpu_contention()
        safety_monitor.verify_nightly_deadline()

        # 4. Search literature for background grounding
        logger.info("Running unified literature search phase...")
        query = f"biomaterial hybrid design and protein coordination for {campaign_name}"
        grounding_evidence = literature.search(query, limit=10)
        logger.info(f"Grounding complete: {len(grounding_evidence)} papers retrieved.")

        # Filter keys for load_lab_config to prevent ConfigError due to custom bridge configs
        lab_config_keys = {"id", "name", "domain", "evidence_sources", "capabilities", "safety_rules", "resources", "preferred_metrics", "human_approval_required_for", "safety_hooks", "description", "version"}
        filtered_config = {k: v for k, v in config.items() if k in lab_config_keys}
        lab_config = load_lab_config(filtered_config)
        lab_state = lab_state_from_config(lab_config)

        # 5. Generación Bruta (KISS high-frequency)
        logger.info("Phase 1: High-throughput async hypothesis generation...")
        raw_candidates = await brute_gen.generate_variants_async(
            goal=f"Design an optimized protein cage interface with high binding affinity and low Ihara complexity for {campaign_name}",
            lab=lab_config,
            prior_evidence=grounding_evidence,
            count=10
        )

        if not raw_candidates:
            logger.error("No candidates survived the falsifier. Halting research cycle.")
            return

        # Log generations to safety monitor
        for h in raw_candidates:
            safety_monitor.log_generation(h.statement)

        # 6. Surrogate World Model Selection (UCB + Exploration pruning)
        logger.info("Phase 2: Surrogate World Model pruning...")
        selected_candidates = world_model.select_top_k(raw_candidates, k=max_experiments, beta=0.5, eps=0.25)
        logger.info(f"Selected {len(selected_candidates)} hypotheses for experimental verification.")

        # 7. Co-Scientist Peer-Review and Ranking
        logger.info("Phase 3: LLM Peer-Review and Ranking...")
        review_batch = reasoning_bridge.review(selected_candidates, lab_config)
        ranked_hyps = reasoning_bridge.rank(selected_candidates, review_batch.reviews)

        # 8. Compile and Execute physical experiments
        logger.info("Phase 4: Compile and execute experiments...")
        all_plan_outcomes = []
        for idx, hyp in enumerate(ranked_hyps):
            logger.info(f"--- Processing hypothesis [{idx+1}/{len(ranked_hyps)}]: {hyp.id} ---")
            
            # Save hypothesis details to ledger
            ledger.save_hypothesis({
                "id": hyp.id,
                "statement": hyp.statement,
                "rationale": hyp.rationale,
                "novelty_claim": hyp.novelty_claim,
                "test_strategy": hyp.test_strategy,
                "status": hyp.status.value,
                "score": hyp.score
            })

            # Create specific biophysics steps for Fibromialgia, Nipah or Ferritin
            steps = []
            stmt_lower = hyp.statement.lower()
            
            # Determine target
            target = "MOR"
            if "adrb2" in stmt_lower:
                target = "ADRB2"
            elif "drd2" in stmt_lower:
                target = "DRD2"
            elif "agtr1" in stmt_lower:
                target = "AGTR1"
            elif "gfp" in stmt_lower:
                target = "GFP"
            elif "alb" in stmt_lower:
                target = "ALB"
            elif "ms4a2" in stmt_lower:
                target = "MS4A2"
                
            # Determine drug
            drug = "naltrexone"
            if "atorvastatin" in stmt_lower:
                drug = "atorvastatin"
            elif "morphine" in stmt_lower:
                drug = "morphine"
            elif "fentanyl" in stmt_lower:
                drug = "fentanyl"
            elif "buprenorphine" in stmt_lower:
                drug = "buprenorphine"
            elif "naloxone" in stmt_lower:
                drug = "naloxone"

            if "fibromialgia" in campaign_name.lower() or "fibromyalgia" in campaign_name.lower() or "ruta_b" in campaign_name.lower():
                # Get sequences for homology alignment
                seq1 = fasta_sequences.get(target, "MALWMRLLPLLALLALWGPDPAAA")
                seq2 = seq1
                if len(seq1) > 20:
                    seq2 = seq1[:20] + "X" + seq1[21:]
                
                seq1_short = seq1[:40]
                seq2_short = seq2[:40]

                steps.append(ExperimentStep(
                    name="predict-dti",
                    action="dti.predict",
                    resource="mammal_local",
                    parameters={"target": target, "drug_name": drug}
                ))
                steps.append(ExperimentStep(
                    name="fold-complex",
                    action="structure.fold",
                    resource="colab_bridge",
                    parameters={"target": target, "method": "alphafold2"},
                    depends_on=["predict-dti"]
                ))
                steps.append(ExperimentStep(
                    name="monitor-preprints",
                    action="literature.monitor_preprints",
                    resource="mammal_local",
                    parameters={"query": f"{target} receptor ligand binding fibromyalgia", "limit": "3"}
                ))
                steps.append(ExperimentStep(
                    name="query-experimental",
                    action="target.query_affinity_experimental",
                    resource="mammal_local",
                    parameters={"target": target, "drug_name": drug}
                ))
                steps.append(ExperimentStep(
                    name="align-homology",
                    action="sequence.align_homologs",
                    resource="topological_auditor",
                    parameters={"seq1": seq1_short, "seq2": seq2_short}
                ))
            elif "nipah" in campaign_name.lower() or "receptor" in hyp.statement.lower():
                steps.append(ExperimentStep(
                    name="predict-dti",
                    action="dti.predict",
                    resource="mammal_local",
                    parameters={"target": "nipah", "drug_name": "naltrexone"}
                ))
                steps.append(ExperimentStep(
                    name="fold-complex",
                    action="structure.fold",
                    resource="colab_bridge",
                    parameters={"target": "nipah", "method": "alphafold2"},
                    depends_on=["predict-dti"]
                ))
                # Add Phase 8 advanced scientific steps
                steps.append(ExperimentStep(
                    name="monitor-preprints",
                    action="literature.monitor_preprints",
                    resource="mammal_local",
                    parameters={"query": "nipah virus receptor binding", "limit": "3"}
                ))
                steps.append(ExperimentStep(
                    name="query-experimental",
                    action="target.query_affinity_experimental",
                    resource="mammal_local",
                    parameters={"target": "nipah", "drug_name": "naltrexone"}
                ))
                steps.append(ExperimentStep(
                    name="align-homology",
                    action="sequence.align_homologs",
                    resource="topological_auditor",
                    parameters={"seq1": "MALWMRLLPLLALLALWGPDPAAA", "seq2": "MALWMRLLPLLALLALWGPDPCAA"}
                ))
            else:
                # Ferritin / BioMaterial steps
                steps.append(ExperimentStep(
                    name="audit-mesh",
                    action="topology.audit",
                    resource="topological_auditor",
                    parameters={"target": "ferritin", "target_seq": "MSGLQPHISV"}
                ))
                steps.append(ExperimentStep(
                    name="dti-cage",
                    action="dti.predict",
                    resource="mammal_local",
                    parameters={"target": "ferritin", "drug_name": "gold_atom"},
                    depends_on=["audit-mesh"]
                ))
                # Add Phase 8 advanced scientific steps
                steps.append(ExperimentStep(
                    name="monitor-preprints",
                    action="literature.monitor_preprints",
                    resource="mammal_local",
                    parameters={"query": "ferritin gold nanoparticle", "limit": "3"}
                ))
                steps.append(ExperimentStep(
                    name="query-experimental",
                    action="target.query_affinity_experimental",
                    resource="mammal_local",
                    parameters={"target": "mor", "drug_name": "naltrexone"}
                ))
                steps.append(ExperimentStep(
                    name="align-homology",
                    action="sequence.align_homologs",
                    resource="topological_auditor",
                    parameters={"seq1": "MSGLQPHISV", "seq2": "MSGLQPHLSV"}
                ))

            spec = ExperimentSpec(
                id=f"spec_{hyp.id}",
                lab_id=lab_config.id,
                objective=hyp.test_strategy,
                hypothesis_id=hyp.id,
                steps=steps,
                safety_constraints=lab_config.safety_rules
            )

            # Compile
            plan = compiler.compile(spec, lab_config, lab_state)
            
            # Execute
            if plan.ok:
                outcome = executor.execute(plan, hyp.id)
                all_plan_outcomes.append(outcome)
                # Log score to safety monitor
                res_values = outcome.get("results", {}).values()
                best_s = max([v.get("pkd", v.get("ihara_zeta", 0.0)) for v in res_values if isinstance(v, dict)], default=0.0)
                safety_monitor.log_score(best_s)
            else:
                logger.error(f"Plan compilation errors: {plan.errors}")
                ledger.save_result(hyp.id, "error", error_msg=", ".join(plan.errors))

        # 9. Tick World Model shadow mode metrics
        world_model.tick_shadow_cycle()

        # 10. Generate morning report REPORTE_MANANA.md
        logger.info("Generating morning report...")
        elapsed_min = (time.time() - t_start) / 60
        report = generate_morning_report(campaign_name, ranked_hyps, all_plan_outcomes, elapsed_min, safety_monitor)
        
        # Write to run results folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_results_dir = LAB_DIR / "automated_lab" / "results" / f"eac_{campaign_name}_{timestamp}"
        run_results_dir.mkdir(parents=True, exist_ok=True)
        (run_results_dir / "REPORTE_MANANA.md").write_text(report)
        logger.info(f"Morning report written successfully to: {run_results_dir / 'REPORTE_MANANA.md'}")

    finally:
        # 11. Release locks
        safety_monitor.release_lock()
        logger.info(f"Campaign complete in {(time.time() - t_start)/60:.2f} minutes.")

def generate_morning_report(campaign_name: str, hypotheses: list, outcomes: list, elapsed_min: float, safety: WSLSafetyMonitor) -> str:
    lines = [
        f"# REPORTE MATUTINO EaC BRIDGE — {campaign_name.upper()}",
        f"**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Autonomía nocturna:** {elapsed_min:.2f} minutos",
        f"**Ejecución:** WSL2 + CUDA MAMMAL local + Colab + Cadena CAD",
        "",
        "## Resumen de Hipótesis y Afinidades Evaluadas",
        "",
        "| ID | Declaración / Propuesta | Score UCB | Afinidades / Métricas Reales | Status |",
        "|---|---|---|---|---|"
    ]

    for h in hypotheses:
        # Retrieve actual result from outcome if exists
        metrics_str = "No ejecutado (compilación fallida)"
        for o in outcomes:
            if o.get("experiment_id") == f"spec_{h.id}":
                results = o.get("results", {})
                parts = []
                for step, res in results.items():
                    if "pkd" in res:
                        parts.append(f"MAMMAL pKd={res['pkd']:.2f}")
                    if "ihara_zeta" in res:
                        parts.append(f"Ihara={res['ihara_zeta']:.2f}")
                    if "real_pkd" in res:
                        parts.append(f"Real pKd={res['real_pkd']:.2f}")
                    if "bias" in res:
                        parts.append(f"Bias={res['bias']:.2f}")
                    if "preprints_count" in res:
                        parts.append(f"Preprints={res['preprints_count']}")
                    if "percent_identity" in res:
                        parts.append(f"SeqId={res['percent_identity']:.1f}%")
                metrics_str = ", ".join(parts) if parts else "Completado"

        lines.append(
            f"| {h.id} | {h.statement[:80]}... | {h.score:.2f} | {metrics_str} | {h.status.value} |"
        )

    lines.extend([
        "",
        "## Monitoreo de Seguridad de Auditoría (Harness)",
        f"- **Modo de supervisión:** {safety.mode}",
        f"- **Llamadas de razonamiento:** {safety.total_calls} total, {safety.error_count} errores",
        f"- **Límite de hora de finalización:** {safety.deadline_hour} AM",
        "",
        "### Firmas de Diagnóstico Registradas",
    ])

    # Query safety audits from SQLite to list violations
    conn_path = Path("artifacts/eac_research_ledger.db")
    if conn_path.exists():
        import sqlite3
        try:
            with sqlite3.connect(conn_path) as conn:
                cursor = conn.execute("SELECT signature, details, verdict, timestamp FROM safety_audits ORDER BY timestamp DESC LIMIT 10;")
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        lines.append(f"- **[{row[0]}]** (Verdict: {row[2]}) at {row[3]}: {row[1]}")
                else:
                    lines.append("- Ninguna firma de fallo activada. Ejecución 100% limpia.")
        except Exception:
            lines.append("- (Error al leer auditorías del Ledger)")
    else:
        lines.append("- No hay auditorías disponibles.")

    lines.extend([
        "",
        "---",
        "*Generado por Antigravity EaC Bridge | DAVI Co-Scientist Swarm + local CAD*",
    ])
    return "\n".join(lines)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Protein Lab EaC Bridge runner")
    parser.add_argument("--campaign", type=str, default="fibromialgia_ruta_b")
    parser.add_argument("--max-experiments", type=int, default=3)
    parser.add_argument("--hours", type=float, default=0.0)
    args = parser.parse_args()

    asyncio.run(run_eac_campaign(args.campaign, args.max_experiments, args.hours))

if __name__ == "__main__":
    main()
