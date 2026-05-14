#!/usr/bin/env python3
"""Monitor and repair automated_lab overnight campaigns.

Designed for Hermes cron every 2 hours. It prints a concise status report every
run. If the scheduler died before completing its budget, it relaunches once with
the same campaign/hours.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

LAB = Path("/home/gris/.hermes/workspace/protein-lab/automated_lab")
RESULTS = LAB / "results"
ACTIVE = RESULTS / "ACTIVE_RUN.json"
STATE = RESULTS / ".overnight_monitor.state.json"
CAMPAIGN = os.getenv("AUTOMATED_LAB_MONITOR_CAMPAIGN", "fibromialgia_ruta_b")
HOURS = float(os.getenv("AUTOMATED_LAB_MONITOR_HOURS", "8"))
MAX_EXPERIMENTS = os.getenv("AUTOMATED_LAB_MONITOR_MAX_EXPERIMENTS", "1600")


def sh(cmd: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def find_scheduler_pids() -> list[str]:
    proc = sh(["ps", "-eo", "pid=,args="], timeout=10)
    pids = []
    needle1 = "python -m engine.scheduler"
    needle2 = f"--campaign {CAMPAIGN}"
    for line in proc.stdout.splitlines():
        if needle1 in line and needle2 in line and "monitor_and_repair" not in line:
            pids.append(line.strip().split(None, 1)[0])
    return pids


def newest_log_tail() -> str:
    logs = sorted((RESULTS / "logs").glob(f"{CAMPAIGN}_*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not logs:
        return ""
    try:
        return "\n".join(logs[0].read_text(errors="replace").splitlines()[-12:])
    except Exception:
        return ""


def relaunch(reason: str) -> str:
    RESULTS.mkdir(parents=True, exist_ok=True)
    cmd = ["bash", "scripts/run_overnight.sh", CAMPAIGN, str(HOURS), MAX_EXPERIMENTS]
    log = RESULTS / "logs" / f"{CAMPAIGN}_repair_{datetime.now().strftime('%Y%m%d_%H%M%S')}.launcher.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "w") as f:
        subprocess.Popen(cmd, cwd=str(LAB), stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
    return f"RELAUNCHED: {reason}; launcher_log={log}"


def main() -> None:
    now = time.time()
    active = load_json(ACTIVE)
    state = load_json(STATE)
    pids = find_scheduler_pids()
    status = active.get("status", "unknown")
    started = float(active.get("started_at_epoch") or 0)
    elapsed_h = ((now - started) / 3600) if started else 0.0
    errors = int(active.get("errors") or 0)
    total = int(active.get("total_results") or active.get("total_experiments") or 0)
    ok = int(active.get("successful") or 0)
    cycle = active.get("cycle", "?")
    batches = active.get("total_batches", "?")
    run_dir = active.get("run_dir", "")

    msg = [
        f"Automated Lab monitor {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"campaign={CAMPAIGN} status={status} pids={','.join(pids) or 'none'} cycle={cycle}/{batches}",
        f"progress={total} results ({ok} ok / {errors} errors) elapsed={elapsed_h:.2f}h run_dir={run_dir}",
    ]

    repair = ""
    if pids:
        repair = "OK: scheduler alive"
    elif status == "completed":
        repair = "OK: campaign completed"
    elif started and elapsed_h < HOURS + 0.5:
        # Avoid relaunch storms: one relaunch per monitor tick interval-ish.
        last_relaunch = float(state.get("last_relaunch_epoch") or 0)
        if now - last_relaunch > 5400:
            repair = relaunch("scheduler missing before time budget ended")
            state["last_relaunch_epoch"] = now
        else:
            repair = "DEAD but relaunch suppressed by cooldown"
    else:
        repair = "No active process; no relaunch because budget expired or ACTIVE_RUN missing"

    state.update({
        "last_checked_at": datetime.now().isoformat(),
        "last_status": status,
        "last_pids": pids,
        "last_run_dir": run_dir,
    })
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    msg.append(repair)
    tail = newest_log_tail()
    if tail:
        msg.extend(["--- log tail ---", tail])
    print("\n".join(msg))


if __name__ == "__main__":
    main()
