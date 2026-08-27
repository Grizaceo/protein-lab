import sqlite3, json, os

db = sqlite3.connect("/home/gris/.hermes/workspace/ACTIVE/agentic-lab-eac/eidos_run_store.db")

# Check what's already there
existing = [r[0] for r in db.execute("SELECT experiment_id FROM experiments").fetchall()]
print("Existing:", existing)

# Load new experiment files
exp_dir = "/home/gris/.hermes/workspace/ACTIVE/protein-lab/experiments"
new_exps = []
for fn in os.listdir(exp_dir):
    if fn.startswith("protein-2") and fn.endswith(".json"):
        path = os.path.join(exp_dir, fn)
        with open(path) as f:
            data = json.load(f)
        eid = data.get("experiment_id", fn.replace(".json",""))
        print(f"  Loading {eid} from {fn}")
        new_exps.append((eid, data, fn))

for eid, data, fn in new_exps:
    if eid in existing:
        print(f"  SKIP {eid} (already in run store)")
        continue
    # Extract fields for run store
    hypothesis = data.get("action", data.get("description", ""))
    spec_hash = data.get("spec_hash", "")
    status = data.get("status", "completed")
    metrics = {k: v for k, v in data.items() if k in ["genes_with_evalue", "COL9A1_evalue", "PTN_evalue", "COL9A1_evalue_lower_ci", "PTN_evalue_lower_ci", "COL9A1_evalue_loo_min", "COL9A1_evalue_loo_max", "COL9A1_evalue_loo_mean", "COL9A1_evalue_loo_std", "verdict"]}
    kill_criteria = data.get("kill_criteria", "")
    result_json = json.dumps(data, ensure_ascii=False)
    now = data.get("timestamp", "2026-08-24T00:00:00")
    try:
        db.execute(
            """INSERT INTO experiments (experiment_id, dominio, hypothesis_text, spec_hash, spec_json, status, kill_criteria_json, metrics_json, result_json, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (eid, "protein", hypothesis, spec_hash, "", status, kill_criteria, json.dumps(metrics, ensure_ascii=False), result_json, now, now)
        )
        print(f"  INSERTED {eid}")
    except sqlite3.IntegrityError:
        print(f"  SKIP {eid} (already exists)")
db.commit()

# Verify
print("\nRun store after update:")
for r in db.execute("SELECT experiment_id, status, datetime(created_at) as ts FROM experiments WHERE dominio='protein' ORDER BY created_at DESC").fetchall():
    print(f"  {r[0]:50s} {r[1]:10s} {r[2]}")
db.close()