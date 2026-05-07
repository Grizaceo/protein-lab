# Instrucciones Colab — Nipah G Binder (2VSM chain A)
**Iteración:** 12  
**Generado:** 2026-04-27 18:59  
**Estrategia:** EXPLOIT  

---

## Estado actual

- Mejor score hasta ahora: **1.0000** (`2026-04-27_mock_nipah_iter10.result`)
- Iteraciones sin mejora (stuck_count): 0

---

## Archivos a subir en Colab

| Archivo local | Ruta en Colab |
| --- | --- |
| `next_run/nipah/target.pdb` | `/content/input/target.pdb` |

> ⚠ PDB no encontrado localmente — descarga manualmente de RCSB

---

## Parámetros a configurar

**Estrategia:** EXPLOIT — EXPLOTAR: última corrida mejoró el score (mejor actual: 1.0000)

| Parámetro | Valor | Razón |
| --- | --- | --- |
| contigs | 90-90 | Longitud del binder |
| hotspot | A489,A504,A505,A506 | Residuos de interfaz objetivo |
| guide_scale | 5 | Fuerza del guidance de hotspot |
| T | 50 | Pasos de difusión |
| num_designs | 8 | Secuencias por backbone |

---

## Pasos

1. Abre el notebook: [https://colab.research.google.com/github/sokrypton/ColabDesign/blob/main/rf/examples/diffusion.ipynb](https://colab.research.google.com/github/sokrypton/ColabDesign/blob/main/rf/examples/diffusion.ipynb)
2. En el menú lateral (carpeta 📁), crea la carpeta `/content/input/`
3. Sube `target.pdb` a `/content/input/target.pdb`
4. En la celda de configuración, ajusta los siguientes valores:

   ```python
   target_pdb  = '/content/input/target.pdb'
   contigs     = '90-90'
   hotspot     = 'A489,A504,A505,A506'
   num_designs = 8
   T           = 50
   guide_scale = 5
   ```

5. `Runtime → Run all` (o Ctrl+F9)
6. Espera ≈45 min (T4 Google Colab)
7. Al terminar, descarga el ZIP resultante
   - Generalmente se llama `test.result.zip` o similar
8. Mueve el ZIP a la carpeta `colab_runs/` del workspace local
9. Ejecuta el loop:

   ```bash
   python lab_iterate.py
   ```

---

## Criterios de éxito (Sappington 2026)

| Métrica | Umbral mínimo | Umbral óptimo |
| --- | --- | --- |
| pLDDT binder | > 0.85 | > 0.90 |
| ipTM (complejo AF2) | > 0.50 | > 0.75 |
| i_pAE | < 15 Å | < 10 Å |
| Rosetta ΔΔG | < −30 REU | < −50 REU |

> **Nota:** Si el notebook no ejecuta scoring de complejo (AF2 multimer),
> el ipTM no estará disponible. En ese caso usar solo pLDDT > 0.90 como
> filtro de primera ronda.

---

## colab_config.json (referencia)

```json
{
  "contigs": "90-90",
  "hotspot_variant": "focal",
  "guide_scale": 5,
  "T": 50,
  "num_designs": 8,
  "hotspot": "A489,A504,A505,A506"
}
```