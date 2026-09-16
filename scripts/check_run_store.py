import sqlite3
db = sqlite3.connect('/home/gris/.hermes/workspace/ACTIVE/agentic-lab-eac/eidos_run_store.db')
rows = db.execute("SELECT experiment_id, status, datetime(created_at) FROM experiments WHERE dominio='protein' ORDER BY created_at DESC").fetchall()
for r in rows:
    print(f'{r[0]:55s} {r[1]:10s} {r[2]}')
db.close()
