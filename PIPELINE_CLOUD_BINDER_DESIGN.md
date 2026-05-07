# Pipeline Cloud-Only: Binder Design Competition Stack
## Fecha: 2026-04-22
## Hardware: RTX 4060 8GB (LOCAL NO APLICA — TODO EN GOOGLE COLAB)

---

## Principio
Tu GPU local no puede correr RFdiffusion (12–24 GB) ni Boltz-2 (16 GB). Todo el pipeline se ejecuta en Google Colab gratuita (GPU T4) + Proteinbase (submit).

---

## Stack Gratuito Verificado

| Tool | URL | GPU Colab | Gratis? | Rol en Pipeline |
|---|---|---|---|---|
| RFdiffusion + ProteinMPNN + AF2 | https://colab.research.google.com/github/sokrypton/ColabDesign/blob/main/rf/examples/diffusion.ipynb | T4 | ✅ Sí | Backbone + Sequence + Validación rápida |
| ColabFold Multimer | https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb | T4 | ✅ Sí | Scoring complejo binder+target |
| Boltz-1 (with restraints) | https://colab.research.google.com/github/cddlab/colabfold_boltz_restr/blob/main/Boltz1.ipynb | T4 High-RAM | ✅ Sí | Scoring avanzado (iTM, pLDDT, ipSAE-like) |
| design-a-protein.com | https://design-a-protein.com/ | N/A (web) | ✅ Sí | Submit directo a Proteinbase |

**NO GRATIS (descartado):**
- BindCraft → pide A100 = Colab Pro ($$$)

---

## Flujo de Trabajo Completo (6 Pasos)

### PASO 1: TARGET PREP (Local o Colab)
Obtén tu target PDB de la competencia (ej: Nipah G, futuros targets).
- Limpia el PDB: conserva solo la cadena target, quita aguas, ligandos irrelevantes.
- Identifica hotspots: residuos expuestos al solvente en la interfaz de binding.
- Guarda `target_clean.pdb`.

### PASO 2: BACKBONE GENERATION (RFdiffusion Colab)
**Notebook:** Sokrypton/ColabDesign RFdiffusion
**URL:** https://colab.research.google.com/github/sokrypton/ColabDesign/blob/main/rf/examples/diffusion.ipynb
**Runtime:** Runtime → Change runtime type → GPU (T4)

**Inputs:**
- `name` = nombre campaña (ej: nipah_binder_01)
- `contigs` = longitud del binder (ej: `70-100` para 70–100 aa)
- `pdb` = sube `target_clean.pdb`
- `iterations` = 50 (default)
- `hotspot` = "A45,A47,A78" (ejemplo residuos target)
- `num_designs` = 20 (grilla básica)

**Outputs:**
- Carpetas `outputs/nipah_binder_01_*/*.pdb` (backbones solo átomos Cα)
- No hay secuencias aún — solo geometría del backbone.

**Tiempo:** ~5 min setup + ~1 min por diseño en T4.

### PASO 3: SEQUENCE DESIGN (ProteinMPNN — Integrado en mismo notebook)
El notebook RFdiffusion de Sokrypton tiene una celda final: "run ProteinMPNN to generate a sequence and AlphaFold to validate".

**Inputs:**
- `num_seqs` = 8 secuencias por backbone
- `mpnn_sampling_temp` = 0.1 (conservador) a 0.3 (diverso)
- `rm_aa` = "C" (quita cisteínas si no quieres puentes disulfuro)

**Outputs:**
- Secuencias FASTA para cada backbone.
- AlphaFold2 single-sequence predicción con pLDDT y pTM.

**Filtros AF2 en este paso:**
- Descarta si pLDDT < 70 (backbone desordenado)
- Descarta si pTM < 0.5 (predicción pobre)

### PASO 4: COMPLEX PREDICTION + SCORING (ColabFold Multimer)
**Notebook:** ColabFold AlphaFold2 Multimer
**URL:** https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb
**Runtime:** T4

**Para cada secuencia candidata:**
- `query_sequence` = `SEQ_BINDER:SEQ_TARGET` (usa `:` como chainbreak)
- Ejemplo: `PIAQI...SK:MGSSHHH...SRA` (binder : target)
- `msa_mode` = mmseqs2_uniref_env
- `pair_mode` = unpaired_paired
- `num_relax` = 0 (más rápido) o 1 (mejor scoring)

**Outputs clave:**
- `ranked_0.pdb` — mejor modelo del complejo
- `pLDDT` — confianza por residuo
- `pTM` — confianza global del complejo
- `ipTM` (interface predicted TM-score) — **métrica clave** para binding

**Filtros ColabFold:**
- Descarta si ipTM < 0.5 (interfaz débil)
- Ideal: ipTM > 0.75 (confianza alta de binding)
- pLDDT de la interfaz > 70

### PASO 4.5: FILTRO ROSETTA DDG (OBLIGATORIO — no omitir)
**Herramienta:** Rosetta `ddg_monomer` o `cartesian_ddg` (disponible en Colab via PyRosetta gratuita para académicos)  
**URL PyRosetta Colab:** https://colab.research.google.com/github/RosettaCommons/PyRosetta.notebooks/blob/master/notebooks/06.08-Docking-and-Design.ipynb

**Criterio de corte:** ΔΔG < −30 REU (~−30 kcal/mol)  
**Base bibliográfica:** Sappington et al., *Nat Commun* 2026, **17**:1101 (DOI: 10.1038/s41467-025-67866-3)  
> Sin este filtro el éxito experimental baja de **9.2% → ~1%**.

**Cómo ejecutar en Colab:**
```python
# Instalar PyRosetta (requiere licencia académica gratuita)
!pip install pyrosettacolabsetup
import pyrosettacolabsetup; pyrosettacolabsetup.install_pyrosetta()

from pyrosetta import *
from pyrosetta.rosetta.protocols.simple_ddg import DdgScanProtocol
init("-ignore_unrecognized_res true -relax:cartesian")

pose_complex = pose_from_pdb("ranked_0.pdb")
# Calcular DDG (ver notebook de referencia para setup completo)
```

**Decisión:**
- ΔΔG < −30 REU → **PASA** (procede a Paso 5)
- ΔΔG ≥ −30 REU → **DESCARTA** (vuelve al Paso 2 con más iteraciones)

### PASO 5: SCORING AVANZADO (Boltz-1 Colab)
**Notebook:** cddlab Boltz-1 with restraints
**URL:** https://colab.research.google.com/github/cddlab/colabfold_boltz_restr/blob/main/Boltz1.ipynb
**Runtime:** T4 High-RAM

**Inputs:**
- `query_sequence` = `SEQ_BINDER:SEQ_TARGET`
- `ligand_input` = dejar vacío (solo proteína)
- `diffusion_samples` = 1
- `recycling_steps` = 3
- `use_restraints` = checked (si tienes restraints)
- `use_boltz_2` = checked (si se te instala, sino usa Boltz-1)

**Outputs:**
- `iTM` — interface TM-score (equivalente a Boltz-2 ipSAE)
- `pLDDT` — per-residue confidence
- `avg_lddt` — promedio
- `confidence_score` — score compuesto

**Filtros Boltz-1 (referencia Nipah):**
- iTM > 0.4 (Adaptyv usó ~0.4 como corte inicial)
- confidence_score > 0.8 para candidatos "seguros"

### PASO 6: SUBMIT A PROTEINBASE
**URL:** https://design-a-protein.com/

**Interfaz web simplificada (actualmente solo target=Nipah G):**
1. Pick Hotspots → selecciona residuos en el target
2. Generate Designs → proteinbase genera diseños automáticamente
3. Send to Lab → submit para síntesis

**Alternativa:** Submit manual via proteinbase.com (subir tus diseños como FASTA).

---

## Métricas Objetivo (basado en Nipah 2026)

| Métrica | Corte Básico | Corte Competitivo | Corte Top 1% |
|---|---|---|---|
| AF2 ipTM | > 0.50 | > 0.75 | > 0.85 |
| Boltz-1 iTM | > 0.40 | > 0.55 | > 0.70 |
| pLDDT interfaz | > 70 | > 80 | > 90 |
| AF2 pTM | > 0.60 | > 0.75 | > 0.85 |
| Boltz confidence | > 0.70 | > 0.80 | > 0.90 |

**Benchmark real Nipah (86% expresaron, 9.6% bind, mejor KD 370 pM):**
- Los diseños con ipSAE (Boltz-2) > top 600 fueron seleccionados para wet lab.
- Top binders tenían ipSAE ~0.8.

---

## Costos Cloud-Only

| Recurso | Costo |
|---|---|
| Google Colab T4 | $0 (gratuito, límite ~12h/session) |
| Proteinbase submit | $0 |
| Proteinbase síntesis/testing | $0 para ti (Adaptyv lo paga en competencias) |

**Limitaciones Colab Gratis:**
- Session timeout: ~12 horas
- GPU T4 puede desconectarse tras inactividad
- High-RAM no siempre disponible (para Boltz-1)
- Solución: Guardar en Google Drive entre sessions

---

## Calendario Competencia

- **Adaptyv Nipah:** Cerró noviembre 2025, resultados publicados enero 2026.
- **Próxima esperada:** Junio–Agosto 2026 (no anunciada aún).
- **CASP16:** Abierto ahora (estructura prediction, NO binder design).

**Acción recomendada ahora:**
1. Practicar pipeline con target Nipah G (datos públicos disponibles).
2. Cuando abra nueva competencia (anuncio en @proteinbase Twitter/LinkedIn), ejecutar pipeline inmediatamente.

---

## Archivos Referenciados
- HANDOFF_PARALIZACION.md — Estado pausado Ruta B (1BFR biosensor)
- Este archivo: PIPELINE_CLOUD_BINDER_DESIGN.md

---
*Pipeline cloud-only verificado para RTX 4060 8GB. Ningun paso requiere computo local.*
