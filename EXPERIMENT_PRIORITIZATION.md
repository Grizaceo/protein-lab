# EXPERIMENT PRIORITIZATION — protein-lab
**Generado:** 2026-06-25 | **Actualizado:** 2026-07-04 (post-auditoria + binder_design)
**Criterio:** Impacto científico / viabilidad técnica / recursos disponibles / tiempo a resultado

---

## P0 — INMEDIATO (línea activa principal)

### P0-0: BindCraft — Validación Nipah G (competencias Adaptyv)
**Score: 20/20** (Impacto 5, Viabilidad 5, Recursos 5, Tiempo 4)

- **Qué:** Migrar de RFdiffusion (ipTM max 0.16) a BindCraft; smoke test 50 traj en Colab
- **Archivos:** `binder_design/` (README, COLAB_INSTRUCTIONS, scripts, configs)
- **Resultado esperado:** ≥1 diseño con ipTM > 0.5 (valida migración de pipeline)
- **Próximo paso:** `python binder_design/scripts/prepare_bindcraft_target.py --mode both` → Colab
- **Bloqueo:** Ejecución manual en Colab (RTX 4060 local no soporta BindCraft)
- **Competencia:** Todas cerradas — modo practicar-y-esperar (`COMPETITION_STATUS.md`)

---

## P0 — INMEDIATO (secundario)

### P0-1: FEP/MM-PBSA D2 vs D3 Selectivity
**Score: 8/20** (Impacto 5, Viabilidad 1, Recursos 5, Tiempo 2) — **CORREGIDO**

- **Estado real:** carpeta `investigacion-fibromialgia/fep/` **NO EXISTE** en disco
- **Acción:** crear scripts desde cero antes de ejecutar; ya no es P0 hasta que exista infra

### P0-2: EAC Automated Lab — Próxima campaña (fibromialgia_ruta_a)
**Score: 17/20** (Impacto 4, Viabilidad 5, Recursos 5, Tiempo 3)

- **Qué:** Lanzar campaña Ruta A (mast cell/IgG targets) con MAMMAL DTI
- **Archivos:** `automated_lab/` completo, `next_run/MOR` como template
- **Resultado esperado:** Nuevos pKd para targets Tier 2-3, posibles candidatos para validación
- **Próximo paso:** Crear campaign_brief para Ruta A, lanzar scheduler overnight
- **Bloqueo:** Ninguno técnico. Solo definir targets y drogas.
- **Tiempo estimado:** 30 min setup, overnight execution
- **Por qué P0:** El automated_lab está operativo y la Ruta A (mastocitos) es la línea con menos datos. Cada corrida genera datos publicables.

---

## P1 — PRÓXIMO (1-2 semanas)

### P1-1: GH7 Baroresistencia — Subir PDB a Kaggle + lanzar Lote 1
**Score: 16/20** (Impacto 4, Viabilidad 4, Recursos 3, Tiempo 5)

- **Qué:** Crear dataset Kaggle con wt_solvated.pdb + mut_solvated.pdb, hacer push de 2 kernels WT
- **Archivos:** `hirondellea-gigas/investigacion-baroresistencia-gh7/` (notebooks listos, EXPERIMENT_HANDOFF.md completo)
- **Resultado esperado:** 2 trayectorias 100ns (WT control + WT hadal) en Kaggle
- **Próximo paso:** Acción manual: crear dataset en Kaggle, subir PDBs, hacer push
- **Bloqueo:** Requiere acción manual en Kaggle (subir PDB). ~10 minutos.
- **Tiempo estimado:** 10 min setup, 2-3 días ejecución Kaggle
- **Por qué P1:** La cuota Kaggle es el limitante. Solo 2 sistemas simultáneos. Pero los kernels están listos.

### P1-2: AlphaFold H. gigas — Fase 4 (proteoma presión extrema)
**Score: 15/20** (Impacto 4, Viabilidad 4, Recursos 3, Tiempo 4)

- **Qué:** Correr AlphaFold2 en Colab para 15 candidatos del proteoma
- **Archivos:** `hirondellea-gigas/colab_alphafold/` (notebook + FASTA listos)
- **Resultado esperado:** 15 estructuras PDB, métricas de calidad
- **Próximo paso:** Subir FASTA a Colab, ejecutar notebook
- **Bloqueo:** Requiere Colab (GPU). Si Colab está ocupado con FEP, esperar.
- **Tiempo estimado:** 2-4 horas en Colab
- **Por qué P1:** Depende de disponibilidad de Colab. Paralelizable con FEP si hay recursos.

### P1-3: Materiales Avanzados — DFT Re-N4C2 d-band center
**Score: 14/20** (Impacto 4, Viabilidad 3, Recursos 3, Tiempo 4)

- **Qué:** Calcular d-band center de Re-N4C2 con GPAW para catalizadores de H2V
- **Archivos:** `materiales-avanzados-chile/run_dft_all.py` (implementado), inputs .gpw listos
- **Resultado esperado:** d-band center vs H2O splitting activity, correlación con literatura
- **Próximo paso:** `python run_dft_all.py` (requiere GPAW + entorno openmm-env)
- **Bloqueo:** GPAW requiere compilación pesada. Verificar si está instalado.
- **Tiempo estimado:** 1-2 días computacionales
- **Por qué P1:** Conecta directamente con la tesis de materiales-avanzados-chile. Si GPAW funciona, es un resultado publicable rápido.

---

## P2 — PLANIFICADO (2-4 semanas)

### P2-1: FEP Producción completa (100ns × 12 sistemas)
**Score: 13/20** (Impacto 5, Viabilidad 3, Recursos 2, Tiempo 3)

- **Qué:** 12 sistemas × 100ns MD + MM-PBSA + FEP completo
- **Depende de:** P0-1 (validación corta primero)
- **Próximo paso:** Si P0-1 es exitoso, escalar a 100ns
- **Recursos:** RTX 4060 (1 sistema a la vez) o Colab Pro A100 (FEP)
- **Tiempo estimado:** 8-12 días (12 × 100ns secuencial) o 3 días con Colab parallel
- **Por qué P2:** Necesita validación previa de P0-1. No lanzar sin confirmar que 10ns funciona.

### P2-2: GH7 Lote 2 (MUT control + MUT hadal)
**Score: 12/20** (Impacto 4, Viabilidad 3, Recursos 2, Tiempo 3)

- **Qué:** Lanzar 2 kernels MUT en Kaggle
- **Depende de:** P1-1 (terminar Lote 1 primero)
- **Próximo paso:** Cuando Lote 1 termine, push MUT kernels
- **Tiempo estimado:** 2-3 días ejecución
- **Por qué P2:** Dependiente de cuota Kaggle. No se puede ejecutar en paralelo con Lote 1.

### P2-3: CASP17 — Registro + primera predicción
**Score: 11/20** (Impacto 4, Viabilidad 2, Recursos 2, Tiempo 3)

- **Qué:** Registrarse en CASP17, correr ColabFold en 1 target
- **Archivos:** `casp17/` (scripts listos: fetch_targets.py, format_submission.py)
- **Próximo paso:** Registro web, descargar target T1234, ejecutar ColabFold
- **Bloqueo:** Requiere registro oficial (posiblemente código de invitación)
- **Tiempo estimado:** 1 día setup, 1-2 días ejecución
- **Por qué P2:** CASP17 es alto impacto pero requiere registro externo. No es urgente si CASP17 está lejos.

---

## P3 — FUTURO (1-3 meses)

### P3-1: H. gigas Sistema Aluminio — BLAST genoma 2025
**Score: 10/20** (Impacto 3, Viabilidad 3, Recursos 2, Tiempo 2)

- **Qué:** BLAST del genoma 2025 para ORF completa de gluconokinasa
- **Depende de:** Disponibilidad del genoma 2025 (Cell)
- **Tiempo estimado:** 1-2 días
- **Por qué P3:** Depende de datos externos. Si el genoma no está público, bloqueado.

### P3-2: Ferritin Biomaterial — Definir hipótesis
**Score: 9/20** (Impacto 3, Viabilidad 2, Recursos 2, Tiempo 2)

- **Qué:** Definir línea de investigación clara para ferritina-Au55
- **Estado:** Carpeta creada, sin hipótesis definida
- **Próximo paso:** Session de ideación → hipótesis testeable
- **Por qué P3:** Sin hipótesis, no hay experimento. No forzar.

### P3-3: Hemoglobina MTR — Definir hipótesis
**Score: 8/20** (Impacto 2, Viabilidad 2, Recursos 2, Tiempo 2)

- **Qué:** Similar a ferritina. Definir qué pregunta se responde.
- **Estado:** Carpeta creada, sin actividad
- **Por qué P3:** Baja prioridad hasta que líneas más maduras avancen.

### P3-4: H. gigas Catálogo General — Fase 4 estructural
**Score: 8/20** (Impacto 2, Viabilidad 2, Recursos 1, Tiempo 3)

- **Qué:** AlphaFold para entradas del catálogo
- **Depende de:** Disponibilidad de Colab
- **Por qué P3:** El catálogo tiene 15+ entradas. AlphaFold es nice-to-have, no bloquea nada.

---

## Experimentos NO priorizados (bloqueados o redundantes)

| Experimento | Bloqueo |
|-------------|---------|
| ESMFold | CRASHEA UBUNTU (16GB VRAM). No usar. Documentado en README. |
| Nav1.8 DTI | Requiere Colab (1956 aa). Baja prioridad vs otros targets. |
| Re SAC CRO dossier | **Auditoria 2026-07-04:** narrativa sin DFT/WHAM/Marcus en disco; TRL real 1-2 |
| Nipah G Binder (RFdiffusion) | **Supersedido por BindCraft** — ver binder_design/ |
| Ferritin Biosensor (RFdiffusion) | Estancado ipTM ~0.06. Depriorizado vs binder_design |
| GH7 MD 100ns | **Auditoria:** trayectorias son ~15 ps, no 100 ns; analisis ausente |

---

## Plan de ejecución recomendado (próximas 2 semanas)

```
Semana 1 (Jun 25 - Jul 2):
├── P0-1: FEP scripts → crear entorno conda, ejecutar 01_prepare_systems.py
├── P0-2: EAC Ruta A → crear campaign_brief, lanzar overnight
└── P1-1: GH7 → acción manual Kaggle (subir PDB), push Lote 1

Semana 2 (Jul 3 - Jul 9):
├── P0-1: Si validación 10ns OK → escalar a 100ns
├── P1-2: AlphaFold H. gigas en Colab (si disponible)
└── P1-3: DFT Re-N4C2 (si GPAW instalado)
```

---

## Métricas de éxito

| Experimento | Métrica | Umbral |
|-------------|---------|--------|
| BindCraft | ipTM | >0.50 = migración OK; >0.75 = competitivo |
| BindCraft | Rosetta ΔΔG | < −30 REU = pasa filtro wet-lab |
| FEP | ΔΔG selectividad D2/D3 | >2 kcal/mol diferencia = selectividad real |
| EAC DTI | pKd nuevo | >7 (sub-100nM) = hit |
| GH7 MD | RMSD convergencia | <3Å después de 50ns |
| AlphaFold | pLDDT | >80 = estructura usable |
| DFT | d-band center | Correlación con literatura (±0.2 eV) |

---

*No ejecutar en orden de prioridad sin verificar recursos disponibles. Si Colab está ocupado, cambiar a local (RTX 4060) o Kaggle según disponibilidad.*
