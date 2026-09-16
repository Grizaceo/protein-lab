import sys
import logging
from pathlib import Path

# Ensure agentic-lab-eac src directory is in sys.path
EAC_SRC = Path("/home/gris96/.hermes/workspace/agentic-lab-eac/src")
if EAC_SRC.exists() and str(EAC_SRC) not in sys.path:
    sys.path.insert(0, str(EAC_SRC))

from agentic_lab_eac.eac import ExperimentCompiler as BaseCompiler
from agentic_lab_eac.models import (
    ExperimentSpec,
    ExecutionPlan,
    LabConfig,
    LabState,
    PlannedCommand
)

logger = logging.getLogger(__name__)

class ProteinLabCompiler(BaseCompiler):
    """
    Extends the ExperimentCompiler from Experiment-as-Code (EaC).
    Validates custom safety rules, GPU capacities, and lowers biophysical
    concepts (MAMMAL DTI, AlphaFold folding, Ihara Zeta topology audits)
    into plans.
    """
    def compile(self, spec: ExperimentSpec, lab: LabConfig, state: LabState) -> ExecutionPlan:
        logger.info(f"Compiling experiment spec {spec.id}...")
        
        # Compile using BaseCompiler to perform standard cycle-detection, capability matching, and safety hook validation
        plan = super().compile(spec, lab, state)

        # Custom biophysics checks and validations
        for cmd in plan.commands:
            # If folding is requested, check if it fits resource capabilities
            if cmd.command.startswith("structure.fold"):
                vram_limit_violated = False
                for r in state.resources:
                    if r.name == cmd.resource:
                        # Check custom low VRAM rules (RTX 4060 VRAM <= 8GB)
                        if "RTX 4060" in r.name or r.attributes.get("vram_gb", 12) <= 8:
                            if "method=esmfold" in cmd.command:
                                vram_limit_violated = True
                
                if vram_limit_violated:
                    plan.errors.append(
                        f"Resource VRAM conflict in {cmd.step_name!r}: ESMFold requires > 8GB VRAM."
                    )
                    plan.warnings.append("Suggested fix: Change folding method to AlphaFold2 via Colab bridge.")

            # Validate Phase 8 Advanced Scientific Skills
            elif cmd.command.startswith("literature.monitor_preprints"):
                if "query=" not in cmd.command:
                    plan.errors.append(
                        f"Missing parameter in {cmd.step_name!r}: 'literature.monitor_preprints' requires 'query'."
                    )
            elif cmd.command.startswith("target.query_affinity_experimental"):
                if "target=" not in cmd.command or "drug_name=" not in cmd.command:
                    plan.errors.append(
                        f"Missing parameter in {cmd.step_name!r}: 'target.query_affinity_experimental' requires 'target' and 'drug_name'."
                    )
            elif cmd.command.startswith("sequence.align_homologs"):
                if "seq1=" not in cmd.command or "seq2=" not in cmd.command:
                    plan.errors.append(
                        f"Missing parameter in {cmd.step_name!r}: 'sequence.align_homologs' requires 'seq1' and 'seq2'."
                    )

        if plan.errors:
            logger.error(f"EaC Compilation FAILED for {spec.id} with {len(plan.errors)} errors.")
        else:
            logger.info(f"EaC Compilation SUCCESSFUL for {spec.id}.")
            
        return plan
