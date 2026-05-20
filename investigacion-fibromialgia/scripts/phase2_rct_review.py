# Mini-Revisión Sistemática: Agonistas Dopaminérgicos en Fibromialgia
# Fase 2 del plan de continuación — Ruta C

"""
Genera la tabla de evidencia clínica y preclinica de agonistas DA en FM,
incluyendo metadatos para el paper.
"""

rct_evidence = [
    # ── Estudios Clínicos ──────────────────────────────────────────────────
    {
        "Tipo": "RCT",
        "Estudio": "Holman & Myers, 2005",
        "PMID": "16052595",
        "DOI": "10.1002/art.21191",
        "Journal": "Arthritis & Rheumatism",
        "Droga": "Pramipexol",
        "Mecanismo": "Agonista D2/D3",
        "N": 60,
        "Diseño": "RCT DB-PC, 14 semanas, mono-centro",
        "Dosis": "Hasta 4.5 mg/día (nocturno)",
        "Outcome_primario": "Dolor VAS",
        "Resultado": "POSITIVO",
        "Efecto": "36% reducción dolor vs 9% placebo; 42% alcanzó ≥50% reducción dolor vs 14% placebo",
        "Outcomes_2": "Fatiga, función física y estado global: todos significativos",
        "Adversos": "Ansiedad transitoria, pérdida de peso; sin abandonos por EAs",
        "Bias_notes": "Mono-centro. Autor (Holman) poseía patentes sobre uso de D2/D3 en FM (conflicto de interés). N pequeño.",
        "Replicado": "NO — sigue siendo el único RCT positivo de un agonista D2/D3 en FM (21 años)",
    },
    {
        "Tipo": "RCT",
        "Estudio": "Holman (pilot), 2003 (unpublished/conference)",
        "PMID": "N/A",
        "DOI": "N/A",
        "Journal": "Presentación ACR",
        "Droga": "Ropinirol",
        "Mecanismo": "Agonista D2/D3",
        "N": 30,
        "Diseño": "Piloto controlado (20 activo / 10 placebo)",
        "Dosis": "No reportada",
        "Outcome_primario": "Dolor",
        "Resultado": "NO SIGNIFICATIVO",
        "Efecto": "Reducción de dolor no alcanzó significancia estadística (p=0.31)",
        "Outcomes_2": "N/A",
        "Adversos": "No reportados en detalle",
        "Bias_notes": "Sin publicación peer-reviewed. Muestra muy pequeña. Mismo investigador que pramipexol.",
        "Replicado": "NO",
    },
    {
        "Tipo": "RCT Fase II",
        "Estudio": "GlaxoSmithKline, NCT00256893",
        "PMID": "N/A (no publicado)",
        "DOI": "N/A",
        "Journal": "GSK Study Register",
        "Droga": "Ropinirol CR",
        "Mecanismo": "Agonista D2/D3",
        "N": 160,
        "Diseño": "RCT DB-PC multicéntrico, 12 semanas",
        "Dosis": "1–24 mg/día (titulación)",
        "Outcome_primario": "Dolor y calidad de vida",
        "Resultado": "NEGATIVO",
        "Efecto": "No alcanzó endpoints primarios. Sin beneficio clínico significativo demostrado.",
        "Outcomes_2": "N/A",
        "Adversos": "No publicados en detalle",
        "Bias_notes": "Trial patrocinado por GSK (fabricante de Requip). Resultados no publicados en revista peer-reviewed — posible sesgo de publicación a la inversa.",
        "Replicado": "N/A — trial negativo",
    },
    # ── Estudios Preclínicos ───────────────────────────────────────────────
    {
        "Tipo": "Preclínico (in vivo)",
        "Estudio": "Peng et al., 2022",
        "PMID": "35799530",
        "DOI": "10.4103/1673-5374.355761",
        "Journal": "Neural Regeneration Research",
        "Droga": "Pramipexol",
        "Mecanismo": "Agonista D3/D2",
        "N": "Ratones (reserpine-induced FM model)",
        "Diseño": "Modelo animal (reserpina), 4 días",
        "Dosis": "Dosis repetidas s.c.",
        "Outcome_primario": "Alodinia mecánica, sensibilidad térmica",
        "Resultado": "POSITIVO (animal)",
        "Efecto": "Inhibición de alodinia mecánica y térmica; restauración de DA en corteza frontal y médula espinal; mejora de comportamiento depresivo",
        "Outcomes_2": "Reducción estrés oxidativo medular (↑SOD)",
        "Adversos": "N/A (modelo animal)",
        "Bias_notes": "Modelo de reserpina replica depleción biogénica pero no el contexto genético/inmune de FM humana.",
        "Replicado": "Confirmatorio de mecanismo, no de eficacia clínica",
    },
]

import pandas as pd

df = pd.DataFrame(rct_evidence)

import pathlib
out_path = str(pathlib.Path(__file__).resolve().parent.parent / "analisis" / "RCT_dopamine_agonists_FM.csv")
df.to_csv(out_path, index=False)

print("=" * 70)
print("MINI-REVISIÓN: AGONISTAS DOPAMINÉRGICOS EN FIBROMIALGIA")
print("=" * 70)

for _, row in df.iterrows():
    print(f"\n{'─'*60}")
    print(f"[{row['Tipo']}] {row['Estudio']}")
    print(f"  Droga:      {row['Droga']} ({row['Mecanismo']})")
    print(f"  N:          {row['N']}")
    print(f"  Diseño:     {row['Diseño']}")
    print(f"  Dosis:      {row['Dosis']}")
    print(f"  Resultado:  {row['Resultado']}")
    print(f"  Efecto:     {row['Efecto']}")
    print(f"  Notas:      {row['Bias_notes']}")
    print(f"  Replicado:  {row['Replicado']}")
    if row['PMID'] != 'N/A':
        print(f"  PMID:       {row['PMID']}")

print(f"\n\nTabla guardada → {out_path}")

# ── Síntesis narrativa ──────────────────────────────────────────────────
print("""
═══════════════════════════════════════════════════════════════════════
SÍNTESIS PARA EL PAPER
═══════════════════════════════════════════════════════════════════════

La evidencia clínica de agonistas dopaminérgicos en FM puede resumirse en
cuatro puntos:

1. ÚNICO RCT POSITIVO (Holman 2005, PMID 16052595):
   Pramipexol (agonista D2/D3, hasta 4.5 mg/día) demostró reducción de
   dolor significativa (36% vs 9% placebo) en 60 pacientes FM.
   42% de pacientes alcanzó ≥50% reducción de dolor (vs 14% placebo).
   Fatiga, función física y estado global también mejoraron.
   ⚠ Limitación: mono-centro, N=60, conflicto de interés (patentes del autor).

2. ROPINIROL FALLIDO (GSK, NCT00256893, N=160):
   El único RCT multicéntrico de un agonista DA (ropinirol CR) fue NEGATIVO.
   No alcanzó endpoints primarios. Resultados nunca publicados en revista 
   peer-reviewed (posible sesgo de publicación negativa).
   Nótese: ropinirol tiene menor afinidad por D3 que pramipexol — diferencia
   farmacológica relevante dado que el GWAS apunta a DRD2 (no DRD3).

3. EVIDENCIA PRECLÍNICA RECIENTE (Peng 2022, PMID 35799530):
   Pramipexol revirtió alodinia y deplección dopaminérgica en modelo
   murino de FM (reserpina), validando el mecanismo D3/D2 en dolor crónico.

4. BRECHA CRÍTICA: EL RCT HOLMAN 2005 NO SE HA REPLICADO EN 21 AÑOS.
   A pesar de un GWAS de 2025 que señala DRD2 como locus de riesgo primario
   en FM, y transcriptómica que muestra DRD2 upregulado en PBMCs de
   pacientes FM, no existe un RCT moderno, adecuadamente potenciado,
   que evalúe pramipexol (o cualquier agonista D2/D3) en FM.
   Esta brecha de 21 años es el principal argumento para nuestro llamado a
   replicación.
""")
