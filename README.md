# 🧬 PROTEIN LAB — Cristóbal
**Fecha diseño:** 2026-04-21
**GPU:** RTX 4060 8GB VRAM | **VRAM confirmable libre:** 7.4 GB

---

## LECCIONES APRENDIDAS (21 abr 2026)

### Causa de los crashes previos
ESMFold requiere ~16GB VRAM para cargar. En RTX 4060 (8GB), agota la memoria → WSL2 se cuelga → Ubuntu se bloquea completamente. NO USAR ESMFold.

### Modelos ESM2 que SÍ funcionan en 8GB

| Modelo | Params | VRAM (embedding) | Uso |
|--------|--------|-----------------|-----|
| ESM2 8M | 7.5M | 0.03 GB | Embeddings rápidos, secuencias largas |
| ESM2 35M | 34M | 0.13 GB | Embeddings de buena calidad |
| ESM2 150M | 148M | 0.59 GB | Embeddings de alta calidad |
| ESM2 650M | 651M | 2.67 GB | Embeddings estado-del-arte |

### Modelos que NO funcionan (requieren >8GB VRAM)
- **ESMFold** (~16GB) — CRASHEA UBUNTU, no usar
- **AlphaFold2** (completo) — borderline, puede funcionar con batch_size=1
- **ColabFold + AlphaFold** — requiere módulo alphafold instalable

---

## STACK CONFIRMADO OPERATIVO

```
Environment: protein-lab (conda)
Python: 3.10.20
GPU: RTX 4060 8GB, VRAM libre ~7.4 GB

Paquetes instalados:
- fair-esm 2.0.0 ✅ (ESM2 embeddings)
- colabfold 1.6.1 ✅ (sin alphafold, modo CPU/lite)
- openfold 2.2.0 (editable) ⚠️ (imports tienen problemas)
- torch 2.6.0+cu124 ✅
- jax 0.6.2 ✅
```

---

## EXPERIMENTOS DISEÑADOS

### Exp 1: Embeddings de hemoglobina con ESM2 (SEGURA)
- **Objetivo:** Generar embeddings de secuencia proteica
- **Entrada:** Hemoglobina humana (P68871, 147 aa)
- **Modelos:** 8M, 35M, 150M, 650M
- **VRAM:** <3 GB total
- **Estado:** PENDIENTE

### Exp 2: Visualización de embeddings (SEGURA)
- **Objetivo:** PCA/t-SNE de embeddings ESM2
- **Entrada:** Resultados de Exp 1
- **Estado:** PENDIENTE

### Exp 3: ColabFold standalone (SEGURA - sin alphafold)
- **Objetivo:** Predicción de estructura sin AlphaFold
- **Método:** Modo `--custom-template` o búsqueda local
- **Nota:** ColabFold sin alphafold es limitado, revisar docs
- **Estado:** REVISAR DOCUMENTACIÓN

### Exp 4: AlphaFold2 (BAJO RIESGO)
- **Objetivo:** Predicción completa de estructura
- **VRAM:** ~6-7 GB con batch_size=1
- **Requisito:** Instalar alphafold desde repo (no pip)
- **Precaución:** Empezar con secuencias cortas, monitoriar VRAM
- **Estado:** FUTURO

---

## REGLAS DE OPERACIÓN (CRÍTICAS)

1. **NUNCA correr ESMFold** — crashea Ubuntu
2. **Antes de correr modelos grandes**, verificar VRAM disponible con `nvidia-smi`
3. **Secuencias >500 aa:** usar modelos pequeños (8M/35M) para embedding
4. **VRAM guard:** si modelo requiere >7GB, no correr en la sesión activa de Hermes
5. **Monitoriar:** después de cada experimento, verificar `torch.cuda.empty_cache()`

---

## Activate

```bash
source ~/.hermes/workspace/protein-lab/activate.sh
```

Este script activa el entorno conda `protein-lab`.
