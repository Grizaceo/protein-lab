# Experimento 01: Predicción CASP17 Target T1364

**Fecha:** 2026-06-20  
**Investigador:** Antigravity (AI Assistant)  
**Workspace:** `protein-lab`  
**Hardware:** RTX 4060 8GB VRAM (Host: Windows, Sandbox: WSL2 Ubuntu)

---

## 1. Selección del Target CASP17
- **Target ID:** T1364
- **Organismo:** *Arabidopsis thaliana* (UniProt ID: A0A178UXU6)
- **Longitud de Secuencia:** 86 residuos
- **Secuencia FASTA:**
  ```fasta
  >T1364 A0A178UXU6, Arabidopsis thaliana, 86 residues|
  DSKLTELNESRAELLNRIQNLKQDLQSWRGKLDTQVKVYREELSGLKKTLNLEVEQLREEFKDLKTTLNQQQDDVSASLKSLGLQD
  ```
- **Razón de Selección:** De los 21 targets tipo proteína monomer/homomer (T) activos, T1364 es el de menor longitud de residuos (86 aa). Esto minimiza drásticamente la demanda de VRAM, haciéndolo ideal para la GPU RTX 4060 (8GB) con ~3.1 GB de VRAM libre al inicio.

---

## 2. Resultados de Embeddings ESM2
Ejecutamos el script personalizado `casp17/scripts/extract_esm2_embeddings.py` para generar embeddings per-residuo usando el modelo de lenguaje de proteínas **ESM2-650M** (`esm2_t33_650M_UR50D`).

- **Parámetros del modelo:** 33 capas transformer, 650 millones de parámetros, dimensión oculta de 1280.
- **Monitoreo de GPU (nvidia-smi):**
  - VRAM libre inicial: **2921 MB** (se ejecutó `torch.cuda.empty_cache()` al inicio por seguridad al ser <3 GB).
  - VRAM con modelo cargado: **727 MB** (consumo del modelo: ~2.19 GB).
  - VRAM final (limpio): **3366 MB**.
- **Tiempos de ejecución:**
  - Carga del modelo en GPU: **12.89 segundos**.
  - Inferencia (forward pass): **0.7191 segundos**.
- **Resultado del Tensor:**
  - Tensor guardado: `casp17/predictions/T1364_esm2_embeddings.pt`
  - Dimensiones: **`86 x 1280`** (per-residue representations, sin tokens especiales de inicio/fin).

---

## 3. Intento de Predicción con ColabFold
Ejecutamos `colabfold_batch` en modo local para predecir la estructura tridimensional del target T1364.

- **Resultado:** **Fallo de importación**
- **Error Detallado:**
  ```traceback
  Traceback (most recent call last):
    File "/home/gris/.miniconda/envs/protein-lab/bin/colabfold_batch", line 3, in <module>
      from colabfold.batch import main
    File "/home/gris/.miniconda/envs/protein-lab/lib/python3.10/site-packages/colabfold/batch.py", line 43, in <module>
      from alphafold.common import protein, residue_constants
  ModuleNotFoundError: No module named 'alphafold.common'
  ```
- **Diagnóstico:**
  - ColabFold local requiere la biblioteca `alphafold` instalada.
  - La instalación editable de `openfold` (v2.2.0) apunta al directorio de trabajo local `/home/gris/.hermes/workspace/protein-lab/openfold`, que está **completamente vacío** (no se clonó el submódulo o repositorio).
  - Dado que la importación falla a nivel de script principal (`colabfold/batch.py`), no es posible evadir este error usando parámetros CLI como `--templates-only` o `--no-amber` (Opción A).

---

## 4. Validación del Formateo CASP TS
Para asegurar el correcto funcionamiento del pipeline de formateo de sumisiones a CASP17, se utilizó un PDB dummy de control (`colab_runs/2026-04-22_test_bmu6c/raw/outputs/test_bmu6c_0.pdb`, 400 líneas ATOM) ejecutando el script `format_submission.py`.

- **Comando:**
  ```bash
  python casp17/scripts/format_submission.py --pdb colab_runs/2026-04-22_test_bmu6c/raw/outputs/test_bmu6c_0.pdb --target T1364 --model 1
  ```
- **Resultado:**
  - Archivo TS generado exitosamente en `casp17/submissions/T1364_model1.ts`.
  - Contiene las cabeceras estándar de CASP17: `PFRMAT TS`, `TARGET T1364`, `AUTHOR XXXX-XXXX-XXXX`, `METHOD ColabFold local prediction on RTX 4060`, `MODEL 1`, `PARENT N/A`.
  - Coordenadas formateadas y líneas `ATOM` correctamente alineadas y con relleno (padding) a 80 caracteres.
  - Terminación correcta con marcadores `TER` y `END`.

---

## 5. Próximos Pasos Sugeridos (Alternativa Google Colab)
Dado que ColabFold no funciona de forma local debido a la falta del paquete de AlphaFold, se propone el siguiente flujo alternativo:

1. **Predicción en Google Colab:**
   - Abrir el cuaderno oficial de ColabFold: [ColabFold: AlphaFold2 using MMseqs2](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb).
   - Introducir la secuencia de T1364 en el campo `query_sequence`.
   - Ejecutar el entorno utilizando una GPU T4 o A100.
   - Configurar `use_amber` a `True` para relajar el modelo y mejorar la física de las cadenas laterales.
   - Descargar el archivo `.zip` resultante al finalizar.
2. **Procesamiento de resultados:**
   - Colocar el ZIP en la carpeta `colab_runs/`.
   - Ejecutar `python process_colab_run.py` para extraer métricas y actualizar el índice del proyecto.
3. **Formateo final:**
   - Extraer el PDB mejor calificado (rango 1) y formatearlo usando `format_submission.py` para obtener el archivo TS final listo para envío.

---

## 6. Lecciones Aprendidas
1. **Verificación de dependencias locales:** El entorno conda `protein-lab` tiene registros de instalaciones de `openfold` y `colabfold` pero carece de los repositorios de soporte requeridos (las carpetas locales están vacías), limitando el uso local de ColabFold.
2. **Seguridad en VRAM:** El modelo ESM2-650M funciona perfectamente en GPUs de 8GB como la RTX 4060, consumiendo alrededor de 2.2 GB de VRAM. Limpiar la caché (`torch.cuda.empty_cache()`) es una práctica crítica que asegura la ejecución exitosa de la inferencia bajo restricciones de memoria.
