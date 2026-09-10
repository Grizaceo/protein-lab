#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Actualizar kanban: protein-gse324210-module-vo2 -> completed con veredicto KILL 2/2."""
import json
from datetime import datetime, timezone

KB = "/home/gris/.hermes/workspace/ACTIVE/kanban.json"
now = datetime.now(timezone.utc).isoformat()

with open(KB) as f:
    kb = json.load(f)

tasks = kb["labs"]["protein-lab"]["tasks"]
for t in tasks:
    if t["id"] == "protein-gse324210-module-vo2":
        t["status"] = "completed"
        t["result"] = (
            "2026-09-10: KILL CONFIRMADO 2/2 sets (spec v2 criterio completo). "
            "GSE111554 blood rho=-0.078 p=0.74 (n=20); GSE111552 PBMC rho=0.190 p=0.48 (n=16). "
            "Ambos FAIL (rho<0.2). GSE324210 delta-VO2 NO testeable: GEO sin vo2peak individual, "
            "paper solo medias por sexo, suplemento figshare tras AWS WAF. "
            "Sub-hipotesis FME (modulo pre-training predice delta-VO2) muerta en sangre basal 2/2 tejidos. "
            "Commit d21054d. Siguiente: eje TAC1/MRGPRX2 en FM (GSE334369) o cohorte humeda."
        )
        t["updates"] = t.get("updates", [])
        t["updates"].append(f"{now} eidos: KILL 2/2 sets confirmado, commit d21054d")
        break

kb["updated"] = now
with open(KB, "w") as f:
    json.dump(kb, f, ensure_ascii=False, indent=1)

# read-back
with open(KB) as f:
    kb2 = json.load(f)
for t in kb2["labs"]["protein-lab"]["tasks"]:
    if t["id"] == "protein-gse324210-module-vo2":
        print("status:", t["status"])
        print("result:", t["result"][:120])
