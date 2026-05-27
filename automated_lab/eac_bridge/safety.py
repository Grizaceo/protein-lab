import os
import sys
import time
import fcntl
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from eac_bridge.ledger import ResearchLedger

logger = logging.getLogger(__name__)

class SafetyException(Exception):
    """Raised when a safety constraint in strict mode is violated."""
    pass

class WSLSafetyMonitor:
    """
    WSLSafetyMonitor integrates custom failure signature audits (Harness S01-S06)
    and WSL computational pitfalls (wsl-computational-experiments).
    """
    def __init__(self, ledger: ResearchLedger, config: dict):
        self.ledger = ledger
        self.config = config
        self.lock_file_path = Path(config.get("wsl_autonomy", {}).get("lock_file", "artifacts/eac_wsl_lock.lock"))
        self.lock_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.lock_fd = None

        self.mode = config.get("runtime_monitor_mode", "permissive")
        self.deadline_hour = int(config.get("wsl_autonomy", {}).get("deadline_hour", 9))
        self.min_vram = int(config.get("wsl_autonomy", {}).get("cuda_vram_min_mb", 2000))

        # Harness stats counters
        self.generation_history: List[str] = []
        self.score_history: List[float] = []
        self.error_count = 0
        self.total_calls = 0

    # ══════════════════════════════════════════════════════════════════════════════
    # WSL Pitfalls Prevention
    # ══════════════════════════════════════════════════════════════════════════════

    def acquire_lock(self):
        """Prevent cron overlap by holding an exclusive flock on the lock file (Pitfall #23)."""
        try:
            self.lock_fd = open(self.lock_file_path, "w")
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.lock_fd.write(f"PID: {os.getpid()}\nStarted: {datetime.now().isoformat()}\n")
            self.lock_fd.flush()
            logger.info("Cron lock acquired successfully. No duplicate instances running.")
        except BlockingIOError:
            msg = "CRON OVERLAP DETECTED: Another scheduler instance is already running."
            self.ledger.log_safety_violation("overlap", "S07_overlap", msg, "abort")
            logger.error(msg)
            sys.exit(1)

    def release_lock(self):
        if self.lock_fd:
            try:
                fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
                self.lock_fd.close()
                if self.lock_file_path.exists():
                    self.lock_file_path.unlink()
                logger.info("Cron lock released.")
            except Exception as e:
                logger.error(f"Failed to release cron lock: {e}")

    def check_gpu_contention(self) -> bool:
        """Query nvidia-smi to ensure CUDA is not busy or overloaded (Pitfall #15)."""
        try:
            cmd = ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,nounits,noheader"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if proc.returncode == 0:
                free_memory = int(proc.stdout.strip().split("\n")[0])
                if free_memory < self.min_vram:
                    msg = f"GPU contention warning: Free VRAM is {free_memory}MB, required {self.min_vram}MB."
                    logger.warning(msg)
                    self.ledger.log_safety_violation("gpu", "S08_contention", msg, "logged")
                    return False
                return True
        except Exception as e:
            logger.warning(f"Could not run nvidia-smi: {e}. Bypassing GPU check.")
        return True

    def verify_nightly_deadline(self):
        """Verify we are within the nightly execution window, preventing daytime GPU hogging (Pitfall #7)."""
        curr_hour = datetime.now().hour
        # If it's morning/daytime past the deadline hour (e.g., past 9 AM and before 10 PM)
        if 9 <= curr_hour < 22:
            msg = f"NIGHTLY DEADLINE REACHED: Current hour is {curr_hour}, window closes at {self.deadline_hour} AM."
            logger.error(msg)
            self.ledger.log_safety_violation("deadline", "S09_deadline", msg, self.mode)
            if self.mode == "strict":
                raise SafetyException(msg)

    # ══════════════════════════════════════════════════════════════════════════════
    # Harness Signatures (S01-S06)
    # ══════════════════════════════════════════════════════════════════════════════

    def log_llm_call(self, success: bool):
        self.total_calls += 1
        if not success:
            self.error_count += 1
        
        # Check S02: High Error Rate (>30% failures after 5 calls)
        if self.total_calls >= 5:
            error_rate = self.error_count / self.total_calls
            if error_rate > 0.3:
                msg = f"High error rate detected in LLM reasoning calls: {error_rate*100:.1f}% failures."
                self.ledger.log_safety_violation("llm", "S02_high_error", msg, self.mode)
                if self.mode == "strict":
                    raise SafetyException(msg)

    def log_generation(self, statement: str):
        self.generation_history.append(statement)
        # Check S01: Loop/Duplicate generation detection (same hypothesis generated multiple times)
        if self.generation_history.count(statement) >= 3:
            msg = f"LOOP DETECTED: Hypothesis generated 3 times or more: {statement!r}"
            self.ledger.log_safety_violation("loop", "S01_loop", msg, self.mode)
            if self.mode == "strict":
                raise SafetyException(msg)

    def log_score(self, best_score: float):
        self.score_history.append(best_score)
        # Check S03: Stalled progress (No score improvement after 3 iterations)
        if len(self.score_history) >= 4:
            recent_scores = self.score_history[-4:]
            if recent_scores[0] >= recent_scores[1] >= recent_scores[2] >= recent_scores[3]:
                msg = f"STALLED PROGRESS DETECTED: Best score has not improved for 3 iterations: {recent_scores}"
                self.ledger.log_safety_violation("stalled", "S03_stalled", msg, self.mode)
                if self.mode == "strict":
                    raise SafetyException(msg)
