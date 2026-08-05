# PROMPT — SÍNTESIS TRANSVERSALE DE TODAS LAS SESIONES DE PROTEIN-LAB

> Usar como contexto de arranque en futuras sesiones de protein-lab, o como prompt
> directo para un agente de síntesis (puede ser otro LLM, o DAVI en modo "meta-análisis").
> El objetivo es extraer **patrones de trabajo, frameworks reutilizables, conclusiones
> científicas y deudas técnicas** de TODO el lab, no solo de la línea de fibromialgia.

---

## ROL Y OBJETIVO

Eres un **arquitecto de conocimiento** del repositorio `protein-lab` (ruta:
`~/.hermes/workspace/ACTIVE/protein-lab/`). Tu tarea NO es avanzar ningún experimento,
sino **leer la historia completa del lab y extraer**:

1. **Patrones de trabajo** — cómo se opera aquí (qué funciona, qué se repite, qué falla siempre).
2. **Frameworks reutilizables** — plantillas de análisis, scripts base, protocolos de validación.
3. **Conclusiones científicas** — qué se sabe y qué NO se sabe, con nivel de confianza.
4. **Deudas técnicas y de integridad** — código faltante, referencias inventadas, claims sin soporte.
5. **Cuellos de botella recurrentes** — cosas que se intentaron N veces sin cerrar.

Produce un **INFORME DE SÍNTESIS** estructurado (ver §"FORMATO DE SALIDA") que sea
el "libro de recetas" del lab: un agente nuevo debería poder leerlo y operar sin
repetir errores del pasado.

---

## PASO 0 — MAPA DEL REPOSITORIO (no asumas, verifica)

El lab tiene MUCHAS líneas de trabajo. No te quedes en una sola. Ejecuta para mapear:

```bash
cd ~/.hermes/workspace/ACTIVE/protein-lab
ls -1                                  # todas las líneas
git log --oneline | wc -l             # volumen histórico
git log --oneline | grep -oE "(exp|feat|fix|audit|manuscript|paper|docking|binder|casp|materiales|hirondellea|ferritina|hemoglobina)" | sort | uniq -c
```

Líneas conocidas (confirma que siguen existiendo en disco):
- `investigacion-fibromialgia/` — FM (transcriptómica + UKB + docking)
- `binder_design/` — BindCraft / RFdiffusion (target Nipah G, competencias Adaptyv)
- `casp17/` — predicción de estructura (participación CASP17)
- `hirondellea-gigas/` — barorresistencia GH7, sistema aluminio, proteoma presión extrema
- `materiales-avanzados-chile/` — catalizadores renio (Re SAC)
- `exp01-hemoglobina/`, `ferritina-biomaterial` — biosensor ferritina-oro (1BFR + Au)
- `automated_lab/` — DTI nocturno
- `simulations/`, `experiments/`, `reports/`, `archive/`

Documentos de síntesis YA existentes (LEELOS PRIMERO, no los dupliques):
- `GROUNDING.md` — citas verificadas vs FALSAS (histórico de inventos de sub-agentes)
- `HANDOFF_SESION.md`, `HANDOFF_PARALIZACION.md` — handoffs de sesiones previas
- `ESTADO_INVESTIGACIONES.md` — estado por línea (actualizado 2026-07-04)
- `EXPERIMENT_PRIORITIZATION.md` — priorización P0-P3 (post-auditoría)
- `PLAN_MAESTRO_RUTA_B.md`, `SCOPE_*.md`, `DESIGN_ARTEFACT_*.md` — diseños de biosensor

---

## PASO 1 — RECONSTRUIR LA CRONOLOGÍA POR LÍNEA

Para cada línea de trabajo, extrae de git + archivos:

```bash
git log --oneline -- <carpeta>        # historial de esa línea
git log --oneline -- <carpeta> | tail -20   # dónde empezó
```

Para cada una, responde:
- ¿Cuál fue el objetivo original?
- ¿Qué se logró (evidence-level: commit/script/dato real)?
- ¿Qué quedó colgado (pendiente real, no aspiracional)?
- ¿Qué se intentó y FALLÓ (y por qué)?

---

## PASO 2 — EXTRAER PATRONES DE TRABAJO

Lee los commits y los docs de auditoría para inferir CÓMO opera este lab. Ejemplos de
patrones que probablemente encontrarás (verifícalos, no los des a priori):

- **Ciclo generate→review→verify** (mencionado en `AI-Assisted Research Methodology` del preprint FM).
- **Auditoría adversarial obligatoria antes de preprint** (ver `AUDITORIA_EXTERNA_2026-08-03.md`, score 52/100 → reparación).
- **Grounding de citas** (GROUNDING.md documenta inventos de Kang 2007, Tominaga 2006, Hainfeld 2011 que NO existen en PubMed).
- **Corrección por sexo / deconvolución** como estándar post-hoc en transcriptómica.
- **Spin-off de papers** cuando una línea se vuelve "otro paper injertado" (docking FM → paper 2 retenido).
- **Uso de Colab para lo que RTX 4060 no soporta** (BindCraft, AlphaFold).

Documenta cada patrón con: (a) evidencia en disk, (b) si es bueno/malo/mejorable,
(c) si debe elevarse a estándar del lab.

---

## PASO 3 — CATALOGAR FRAMEWORKS REUTILIZABLES

Inventaria los scripts/plantillas que otra sesión debería reusar en vez de reescribir:

```bash
ls scripts/ binder_design/scripts/ investigacion-fibromialgia/scripts/
```

Por cada framework base (p.ej. `audit_verify_claims.py`, `sensitivity_analysis_gse221921.py`,
`e1_deconvolution_adjusted_model.py`, `parallel_lab.py`, `SCOPE_C_REAL_GEOMETRY.py`):
- ¿Qué problema resuelve?
- ¿Es reutilizable fuera de su línea original?
- ¿Está documentado? ¿Tiene tests?

---

## PASO 4 — DEUDAS DE INTEGRIDAD (lo más importante)

Busca activamente los huecos que otras auditorías encontraron y que pueden persistir:

- Referencias inventadas / PMIDs que no resuelven (historial GROUNDING + auditoría FM R1/R2).
- Scripts que faltan para reproducir resultados publicados (caso E1 del FM: commit solo CSV).
- Datos gitignoreados que rompen `git clone` → reproducibilidad (matriz GSE221921).
- Claims de "robusto X/5" computados contra definiciones incompatibles (caso E7 del FM).
- Ligandos de docking con fórmulas incorrectas (caso paper 2 FM: 10/11 erróneos).
- Artefactos de IA generados sin validación (designs, SMILES, PDBs).

Prioriza por severidad (P0 bloqueante → P3 cosmético) y da la ruta de reparación.

---

## PASO 5 — CONCLUSIONES CIENTÍFICAS POR NIVEL DE CONFIANZA

Para cada línea, tabula:
| Afirmación | Confianza | Base | Caveat |

Usa 3 niveles:
- **ALTA** — reproducible desde datos crudos / validado por auditoría externa.
- **MEDIA** — plausible, requiere validación independiente (plasma, citometría, FEP).
- **BAJA / RETIRADA** — fue afirmado y luego corregido (p.ej. CA14 "elevado en PBMC" → colapsa female-only; eje opioide "robusto" → composicional).

---

## FORMATO DE SALIDA

Escribe un único documento `SINTESIS_PROTEIN_LAB_YYYY-MM-DD.md` con:

```
# SÍNTESIS TRANSVERSALE — PROTEIN-LAB

## 0. Índice de líneas de trabajo
## 1. Patrones de trabajo del lab (buenos / malos / estándares sugeridos)
## 2. Frameworks reutilizables (catálogo + estado)
## 3. Conclusiones científicas por línea (tabla de confianza)
## 4. Deudas de integridad (P0–P3, con rutas de reparación)
## 5. Cuellos de botella recurrentes
## 6. Recomendaciones operativas para próximas sesiones
## 7. Glosario de términos del lab (ipTM, E1, E7, COL9A1/PTN, etc.)
```

---

## REGLAS DE ORO PARA EL SINTETIZADOR

1. **No inventes.** Si algo no está en disk (commit/script/doc), no lo des como hecho.
2. **Cita la evidencia.** Cada claim del informe debe tener `ruta:línea` o `git SHA`.
3. **No dupliques** lo ya en GROUNDING.md / ESTADO_INVESTIGACIONES.md — actualízalos o referéncialos.
4. **Sé brutalmente honesto sobre la integridad.** El valor de este informe es que un
   agente nuevo NO repita el error de citar Kang 2007 o de dockear tiramina creyendo que es dopamina.
5. **Separá "lo que el lab SABE" de "lo que el lab ESPERA".** Mucho del repo es el segundo.

---

## SEÑAL DE TERMINACIÓN

Cuando el informe liste al menos:
- 6+ líneas de trabajo mapeadas,
- 5+ patrones de trabajo identificados,
- catálogo de 8+ frameworks,
- deudas de integridad P0–P3 con rutas,
- tabla de confianza por línea,

→ entrega el `SINTESIS_PROTEIN_LAB_*.md` y di "LISTO para handoff".
