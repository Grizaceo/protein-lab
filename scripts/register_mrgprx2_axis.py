#!/usr/bin/env python3
"""Register ichor-fme-gse334369-mrgprx2-axis-v1 in the run store (read-back included)."""
import sqlite3
import json
import hashlib

ROOT = "/home/gris/.hermes/workspace/ACTIVE"
spec_path = f"{ROOT}/protein-lab/experiments/ichor-fme-gse334369-mrgprx2-axis-v1.json"
data = json.load(open(spec_path))
canon = json.dumps(
    {k: v for k, v in data.items() if k not in ("spec_hash", "hash_method")},
    sort_keys=True, separators=(",", ":"), ensure_ascii=False,
)
spec_hash = "sha256:" + hashlib.sha256(canon.encode()).hexdigest()
data["spec_hash"] = spec_hash
json.dump(data, open(spec_path, "w"), indent=2, ensure_ascii=False)

con = sqlite3.connect(f"{ROOT}/agentic-lab-eac/eidos_run_store.db")
cols = [r[1] for r in con.execute("PRAGMA table_info(experiments)")]
row = {
    "experiment_id": data["experiment_id"],
    "dominio": data["domain"],
    "hypothesis_text": "MRGPRX2/TAC1 axis differentially LPS-responsive in FM neutrophils (GSE334369)",
    "spec_hash": spec_hash,
    "spec_json": json.dumps(data, ensure_ascii=False),
    "status": data["status"],
    "kill_criteria_json": json.dumps(data["kill_criterion"], ensure_ascii=False),
    "metrics_json": json.dumps(data["results"], ensure_ascii=False),
    "result_json": json.dumps(data, ensure_ascii=False),
    "created_at": data["timestamp_utc"],
    "updated_at": data["timestamp_utc"],
    "verification_standard": "scientific",
}
use = {k: v for k, v in row.items() if k in cols}
ph = ",".join("?" * len(use))
con.execute(f"INSERT OR REPLACE INTO experiments ({','.join(use)}) VALUES ({ph})", list(use.values()))
con.commit()
n = con.execute("SELECT COUNT(*) FROM experiments").fetchone()[0]
check = con.execute(
    "SELECT status, spec_hash FROM experiments WHERE experiment_id=?",
    (data["experiment_id"],),
).fetchone()
print("READ-BACK:", check)
print("total rows:", n)
con.close()