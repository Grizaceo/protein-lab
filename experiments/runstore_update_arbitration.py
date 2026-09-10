#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Actualizar run store: ichor-fme-exercise-responder-arbitration-v1 con el segundo set (GSE111552 PBMC)."""
import sqlite3, json
from datetime import datetime, timezone

DB = "/home/gris/.hermes/workspace/ACTIVE/agentic-lab-eac/eidos_run_store.db"
now = datetime.now(timezone.utc).isoformat()

# Resultado del segundo set (verificado en disco)
kill2 = {
    "rho": 0.1898,
    "p": 0.4813,
    "n": 16,
    "dataset": "GSE111552",
    "tissue": "PBMC",
    "threshold": "rho<0.2=FAIL, rho>0.4=PASS",
    "verdict": "FAIL (rho<0.2)"
}
kill1 = {
    "rho": -0.0781954887218045,
    "p": 0.7431490742332264,
    "n": 20,
    "dataset": "GSE111554",
    "tissue": "blood",
    "threshold": "rho<0.2=FAIL, rho>0.4=PASS",
    "verdict": "FAIL (rho<0.2)"
}

new_status = "kill-blunting-vo2-confirmed-2sets-rho-0.078-and-0.190"
new_kill = {
    "sets": [kill1, kill2],
    "summary": "Ambos sets del estudio GSE11155x con vo2peak individual: GSE111554 (blood, n=20) rho=-0.078 p=0.74; GSE111552 (PBMC, n=16) rho=0.190 p=0.48. Ambos FAIL (rho<0.2). Sub-hipotesis FME (modulo genetico pre-training predice delta-VO2) muerta en 2 tejidos independientes.",
    "note": "GSE111553 (blood G1) no trae vo2peak en series matrix -> no testeable. GSE111551 (muscle) fuera de alcance blood."
}
new_result = {
    "analysis_plan": {
        "data": "GSE111554 (blood) + GSE111552 (PBMC), mismo estudio 18wk running, vo2peak pre/post por sujeto",
        "primary_test": "Spearman(module score pre, delta-VO2max)",
        "module": ["CXCL8", "IL6", "IL1B", "TNFAIP3"],
        "threshold": "rho<0.2=FAIL, rho>0.4=PASS (pre-registrado spec v2)"
    },
    "results": {
        "GSE111554_blood": kill1,
        "GSE111552_pbmc": kill2
    },
    "verdict": "KILL CONFIRMADO en 2 sets independientes (blood + PBMC). La expresion pre-training del modulo blunting no predice respuesta VO2max. FME sub-hypothesis dead at blood baseline (2/2 sets)."
}

con = sqlite3.connect(DB)
cur = con.cursor()
cur.execute(
    "UPDATE experiments SET status=?, kill_criteria_json=?, result_json=?, updated_at=? WHERE experiment_id=?",
    (new_status, json.dumps(new_kill, ensure_ascii=False), json.dumps(new_result, ensure_ascii=False), now,
     "ichor-fme-exercise-responder-arbitration-v1")
)
con.commit()
print("rows updated:", cur.rowcount)

# read-back
cur.execute("SELECT status, updated_at FROM experiments WHERE experiment_id='ichor-fme-exercise-responder-arbitration-v1'")
print("read-back:", cur.fetchone())
con.close()
