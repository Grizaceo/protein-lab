# ITERACION 4 — Nipah G Binder (2VSM chain A): PASO A PASO EJECUTABLE
## Generado: 2026-04-25 00:08 | Estrategia: EXPLOIT (focal patch)

---

## PREPARACION (30 seg)

1. Abre COLAB A: Sokrypton RFdiffusion + ProteinMPNN + AF2 single
   https://colab.research.google.com/github/sokrypton/ColabDesign/blob/main/rf/examples/diffusion.ipynb
2. Runtime → Change runtime type → GPU (T4)
3. En el menu lateral (carpeta 📁), crea `/content/input/`
4. Sube `target.pdb` a `/content/input/target.pdb`
5. `Runtime → Run all` (Ctrl+F9)

---

## PASO 1: RFDIFFUSION (celda de config)

```python
name        = "nipah_iter4_focal"
target_pdb  = '/content/input/target.pdb'
contigs     = '90-90'
hotspot     = 'A489,A504,A505,A506'
num_designs = 8
iterations  = 50
guide_scale = 15
T           = 50          # NOTA: next_run dice T=25, pero RFdiffusion oficial usa iterations=50. Deja iterations=50.
```

> ⚠ **CRITICO:** guide_scale=15 es AGRESIVO. Si ves warning "too many hotspot atoms", reduce a 10 en la siguiente. Pero iteracion 4 dice 15 → prueba 15.

Deja que corra (~5 min para 8 backbones).

---

## PASO 2: PROTEINMPNN + AF2 SINGLE (celda final del notebook)

```python
mpnn_sampling_temp = 0.1      # conservador para iteracion exploit
rm_aa = "C"                   # quita cisteinas si no quieres puentes disulfuro
num_seqs = 8
```

Espera (~20 min para 8×8=64 secuencias).

**OUTPUT QUE NECESITAS ANOTAR:**
En `outputs/nipah_iter4_focal/`, abre `mpnn_results.csv` y `best_design.pdb`.
Copia/pega las 3 MEJORES secuencias FASTA con sus pLDDT scores.

---

## PASO 3: MANUAL EXTRACTION (el paso que rompe el loop)

Desde la carpeta outputs de Colab:
1. Descarga `mpnn_results.csv` — tiene nombre + pLDDT + pTM de cada diseño
2. Descarga los `.pdb` de los diseños con pLDDT > 0.85
3. Abre los `.pdb` con un editor del texto o descarga los FASTA

Anota en un archivo local:
```
diseño_0: PIAQILH...SKK (413 aa) pLDDT=0.93 pTM=0.82
diseño_1: LMQGFRD...AVE (413 aa) pLDDT=0.91 pTM=0.79
...
```

---

## PASO 4: COLABFOLD MULTIMER (verdadero complejo scoring)

Abre COLAB B:
https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb

Runtime → GPU (T4)

En la celda de `query_sequence`:
```
PIAQILH...SKK:ICLQKTSNQILKPKLISYTLGQSGTCITDPLLAMDEGYFAYSHLERIGSCSRGVSKQRII...
```
Donde `PIAQILH...SKK` es la SECUENCIA del diseño binder (del PASO 3).
Y después del `:` va la secuencia completa del target 2VSM (abajo).

**Ajustes:**
- msa_mode = mmseqs2_uniref_env
- pair_mode = unpaired_paired
- num_relax = 0 (mas rapido)
- num_models = 5 (default)
- rank_by = ptm

**Secuencia completa del target (2VSM chain A):**
```
ICLQKTSNQILKPKLISYTLGQSGTCITDPLLAMDEGYFAYSHLERIGSCSRGVSKQRII
GVGEVLDRGDEVPSLFMTNVWTPPNPNTVYHCSAVYNNEFYYVLCAVSTVGDPILNSTYW
SGSLMMTRLAVKPKSNGGGYNQHQLALRSIEKGRYDKVMPYGPSGIKQGDTLYFPAVGFL
VRTEFKYNDSNCPITKCQYSKPENCRLSMGIRPNSHYILRSGLLKYNLSDGENPKVVFIE
ISDQRLSIGSPSKIYDSLGQPVFYQASFSWDTMIKFGDVLTVNPLVVNWRNNTVISRPGQ
SQCPRFNTCPEICWEGVYNDAFLIDRINWISAGVFLDSNQTAENPVFTVFKDNEILYRAQ
LASEDTNAQKTITNCFLLKNKIWCISLVEIYDTGDNVIRPKLFAVKIPEQCTH
```

Ejecuta. Espera ~10 min por diseño.

**OUTPUT CRITICO:**
Al finalizar, descarga el ZIP completo de resultados.
El ZIP contiene `ranked_0.pdb` y `result_model_5_ptm.npz` (o similar).

---

## PASO 5: EXTRACCION MANUAL DE METRICAS (otro cuello de botella)

Descomprime el ZIP de ColabFold. Abre `result_model_5_ptm.npz`:
```python
import numpy as np
data = np.load('result_model_5_ptm.npz')
print('ipTM:', data['ipTM'])
print('pTM:', data['pTM'])
print('ranking_confidence:', data['ranking_confidence'])
```

En Colab puedes hacer esto en una celda:
```python
!pip install numpy
import numpy as np, glob
for f in glob.glob('results/*.npz'):
    d = np.load(f)
    print(f, 'ipTM:', d.get('ipTM', 'NO_KEY'))
```

Anota:
- pLDDT del binder (del PDB ranked_0.pdb)
- ipTM del complejo (del NPZ)
- pAE (del NPZ si existe)

---

## PASO 6: ENTREGA A DAVI (cierra el loop)

Mueve el ZIP a `colab_runs/` del workspace:
```bash
# En tu PC local (Windows/WSL):
mv nipah_iter4_colabfold.zip /mnt/c/Users/<tu_usuario>/Downloads/
# Luego en WSL:
mv /mnt/c/Users/<tu_usuario>/Downloads/nipah_iter4_colabfold.zip \
   /home/gris/.hermes/workspace/protein-lab/colab_runs/
```

Luego ejecuta:
```bash
cd /home/gris/.hermes/workspace/protein-lab
python process_colab_run.py nipah_iter4_colabfold.zip
python lab_iterate.py --status
```

Yo analizo, genero iteracion 5, y repetimos.

---

## PARAMS DE REFERENCIA (para copiar directo)

```json
{
  "contigs": "90-90",
  "hotspot_variant": "focal",
  "guide_scale": 15,
  "iterations": 50,
  "num_designs": 8,
  "hotspot": "A489,A504,A505,A506",
  "mpnn_temp": 0.1,
  "rm_aa": "C"
}
```

---

*Fin del documento. No borrar — es el template para la iteracion 4.*
