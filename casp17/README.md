# 🧬 CASP17 (2026) — Guía de Participación y Herramientas

Esta carpeta contiene todo lo necesario para organizar, monitorizar y formatear tus predicciones para la competencia **CASP17 (Critical Assessment of Structure Prediction)** activa durante **abril – agosto de 2026**.

> **⚠️ REQUISITO PREVIO:** Antes de poder enviar predicciones, debes registrarte en el portal oficial y obtener tu código de registro (`XXXX-XXXX-XXXX`). Sin ese código, tus envíos serán rechazados. Ver **Paso 1**.

---

## 📌 Flujo de Trabajo para Participar

### Paso 1: Registro Oficial
1. Regístrate en el portal oficial del *Prediction Center*: [https://predictioncenter.org/casp17/index.cgi](https://predictioncenter.org/casp17/index.cgi) (menú superior, enlace **Registration**).
2. Puedes registrarte como **grupo de predicción humano** (Human Group). Si utilizas modelos computacionales que corres localmente en tu RTX 4060, el registro de grupo humano/manual es adecuado.
3. Al registrarte, recibirás un **código de registro** con formato `XXXX-XXXX-XXXX`. Este código es tu identificador de AUTHOR en todos los envíos. **Guárdalo.**
4. Asegúrate de registrar correctamente la dirección de correo electrónico desde la cual enviarás tus modelos.

### Paso 2: Monitorizar y Descargar Objetivos
1. Ejecuta el script para ver qué objetivos (*targets*) están activos, agrupados por tipo:
   ```bash
   python scripts/fetch_targets.py --list
   ```
   Los targets se clasifican por prefijo: **T** = Proteína, **H** = Heterómero, **R** = RNA, **M** = Multímero, **E** = Ensamblaje.

2. Filtrar por tipo (solo proteínas):
   ```bash
   python scripts/fetch_targets.py --list --type T
   ```

3. Descarga la secuencia FASTA del objetivo que desees resolver:
   ```bash
   python scripts/fetch_targets.py --download T1313
   ```
   *(La secuencia se guardará en `targets/T1313.fasta`)*.

4. Descargar todas las secuencias de un tipo:
   ```bash
   python scripts/fetch_targets.py --download-all --type T
   ```

### Paso 3: Predicción Local (Folding)
Utiliza las herramientas instaladas en tu entorno Conda `protein-lab` para plegar la proteína.
* **ColabFold / AlphaFold:** Corre la predicción usando tu entorno local:
   ```bash
   # Activar entorno
   source ~/.hermes/workspace/protein-lab/activate.sh

   # Ejemplo usando colabfold_batch
   colabfold_batch targets/T1313.fasta predictions/
   ```
   *(Asegúrate de guardar el mejor modelo PDB en `predictions/T1313.pdb`)*.

* **ESM2 Embeddings:** Para generar features complementarias o como input para otros modelos.

### Paso 4: Formatear al estándar CASP TS
CASP requiere que las coordenadas de estructura terciaria (TS) se envíen con cabeceras de texto específicas (`PFRMAT TS`, `TARGET`, `AUTHOR`, `METHOD`, `MODEL`, `PARENT`).

#### Modelo único:
```bash
python scripts/format_submission.py \
  --pdb predictions/T1313.pdb \
  --target T1313 \
  --model 1 \
  --method "ColabFold local prediction on RTX 4060" \
  --parent N/A \
  --author TU-CODIGO-AQUI
```

#### Múltiples modelos (hasta 5, en un solo archivo):
```bash
python scripts/format_submission.py \
  --multi predictions/T1313_rank1.pdb predictions/T1313_rank2.pdb \
  --target T1313 \
  --parent N/A \
  --author TU-CODIGO-AQUI
```

**Parámetros importantes:**
| Parámetro | Descripción |
|-----------|-------------|
| `--model`  | Índice de confianza (1 a 5, siendo 1 el principal evaluado) |
| `--parent` | Templates PDB usados (ej. `1abc_A 2def_B`) o `N/A` si fue *de novo* |
| `--method` | Breve descripción de tu pipeline |
| `--author` | Tu código de registro CASP17 (`XXXX-XXXX-XXXX`) |

### Paso 5: Enviar la Predicción
Tienes dos formas de realizar el envío oficial **antes del vencimiento** del target:
1. **Formulario Web (recomendado):** Sube el archivo `.ts` generado en: [https://predictioncenter.org/casp17/submit](https://predictioncenter.org/casp17/submit).
2. **Vía Correo Electrónico:** Envía un email a:
   * **Destinatario:** `models@predictioncenter.org`
   * **Remitente:** Debe ser la dirección de correo registrada en CASP.
   * **Cuerpo del mensaje:** Pega el contenido de tu archivo `.ts` directamente en texto plano.

> **Nota:** Puedes verificar si tu modelo fue procesado con éxito ingresando al **Model Viewer** de la página de CASP17. No se envía confirmación automática por correo.

---

## 📂 Estructura de la Carpeta

```
casp17/
├── README.md              ← Esta guía
├── scripts/
│   ├── fetch_targets.py   ← Descarga y monitorización de targets
│   └── format_submission.py  ← Formateo PDB → CASP TS
├── targets/               ← Secuencias FASTA descargadas
├── predictions/           ← Modelos PDB de tus predicciones
└── submissions/           ← Archivos .ts listos para enviar
```

---

## 🏷️ Nomenclatura de Targets

| Prefijo | Tipo | Ejemplo |
|---------|------|---------|
| T | Proteína (monómero/homómero) | T1313, T1357 |
| H | Heterómero (complejo proteico) | H1311, H2324 |
| R | RNA | R2301, R2310 |
| M | Multímero | M2310, M2334 |
| E | Ensamblaje | E2366, E2375 |
| W | Whole-cell | W2385, W2386 |

---

## 📋 Formato CASP TS — Referencia Rápida

```
PFRMAT TS                          ← Tipo de formato (obligatorio)
TARGET T1313                       ← ID del target (obligatorio)
AUTHOR XXXX-XXXX-XXXX             ← Código de registro (obligatorio)
METHOD ColabFold prediction ...    ← Descripción libre (obligatorio)
MODEL  1                           ← Índice del modelo 1-5 (obligatorio)
PARENT N/A                         ← Templates usados (obligatorio)
ATOM      1  N   MET A   1 ...    ← Coordenadas PDB (80 chars/línea)
...
TER                                ← Fin de cadena
END                                ← Fin de modelo
```

**Reglas clave:**
- Máximo 5 modelos por archivo. Modelo 1 = evaluación principal.
- Líneas ATOM deben tener 80 caracteres (padding con espacios).
- Solo registros ATOM y TER (no HETATM para proteínas).
- PARENT va **dentro** del bloque MODEL (después de MODEL, antes de ATOM).
- Line endings: LF (Unix). No CRLF.
