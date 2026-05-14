# ARTEFACTO SAIR Summit → Fibromialgia
## Conceptos transferibles del Science x AI Summit 2026

**Fecha:** 2026-05-14
**Fuente:** SAIR Summit transcripts (Palo Alto, May 12-13 2026)
**Objetivo:** Extraer principios del summit aplicables a nuestra pipeline MAMMAL + Fibromialgia

---

## 1. Lewis Tunstall (HuggingFace) — Automated Lab Loop

### Fuente
`Hugging Face's Lewis Tunstall on post-training and open-source AI`, líneas 343-373

### Cita clave
> *"There's now a bunch of different startups like Periodic Labs who are trying to basically create an automated lab so that when the LLM is in the loop, it actually can design experiments, run them semi-autonomously, gets the results from that, and then that's your training loop. You're getting real-world signals as part of the RL process."*

### Aplicación a nuestro proyecto

Estamos haciendo la **mitad computacional** de ese loop:

```
[Nosotros ahora]     MAMMAL DTI → predice pKd → rankea fármacos → ???
[Loop completo]      MAMMAL DTI → predice pKd → rankea fármacos → wet-lab test → feedback al modelo
```

Nuestra tabla de 16 targets con MAMMAL DTI es exactamente el tipo de **priorización** que Tunstall describe: el modelo computacional filtra candidatos, y solo los mejores van a validación experimental.

### Principio extraído: "Testear solo los de mayor prospecto"

Aunque Tunstall no usó esas palabras exactas, el concepto de "closing the lab simulation loop" implica que:
1. El modelo genera hipótesis (candidatos fármaco-target)
2. Solo los top-ranked pasan al wet lab
3. Los resultados experimentales realimentan al modelo

Esto es **exactamente** nuestra pipeline MAMMAL DTI → ranking → priorización.

---

## 2. Lewis Tunstall — Rubrics for Partial Rewards

### Fuente
Líneas 311-340

### Cita clave
> *"In biology, you can't just get a clean answer... One of the most promising methods is rubrics — partial scores from a checklist of grading criteria."*

### Aplicación

Nuestro ranking MAMMAL DTI no es binario (bind/no-bind). Es una **escala continua de pKd** que permite:
- pKd ≥ 8: alta prioridad para validación
- pKd 6-8: prioridad media
- pKd < 6: descartar o baja prioridad

Esto es un "rubric" implícito: no necesitamos un sí/no, tenemos una graduación.

---

## 3. Lewis Tunstall — AlphaFold como precedente

### Fuente
Líneas 660-664

### Cita clave
> *"Things like AlphaFold were all built on top of a large body of preceding work."*

### Aplicación

MAMMAL sigue el mismo patrón que AlphaFold: modelo fundacional pre-entrenado en datos masivos (2B samples), fine-tuned para tareas específicas. Nuestro uso de `dti_bindingdb_pkd` es exactamente ese patrón.

Lección: así como AlphaFold necesitó PDB + UniProt + comunidades abiertas, nosotros necesitamos:
- Nuestros datos limpios (GSE67311, DEGs, targets)
- Un modelo fundacional abierto (MAMMAL)
- Fine-tuning para nuestra tarea específica (DTI → FM)

---

## 4. Terence Tao — Competencias como motor de innovación

### Fuente
`Terence Tao: Mathematics competitions at SAIR`, líneas 28-112

### Cita clave
> *"Traditional venues for doing mathematics are getting saturated by how much AI they can absorb... We need infrastructure: lanes for humans and lanes for AI."*

### Aplicación

El concepto de "lanes" (carriles) es transferible: nuestra pipeline tiene:
- **Carril computacional:** MAMMAL DTI + ESM2 + DEG analysis (rápido, escalable)
- **Carril de validación:** Literatura auditada + PDB verificados + datos GEO (rigor humano)

No mezclamos predicción con validación. Cada una tiene su carril, como Tao propone para matemáticas.

---

## 5. README del Summit — Próximos pasos de SAIR

### Fuente
`README.md`, línea 55

> *"Más competencias en física, química (mencionado por Tao)"*

SAIR está expandiéndose a química. Esto podría significar futuras competencias de drug design o docking que podrían ser directamente relevantes. Estar atentos.

---

## Resumen: Lo que nos llevamos al proyecto

| Concepto del Summit | Aplicación directa en Fibromialgia |
|---------------------|-----------------------------------|
| Automated lab loop (Tunstall) | Pipeline MAMMAL DTI → ranking → priorización para validación |
| Rubrics / partial rewards (Tunstall) | Escala pKd (no binaria) para rankear fármacos |
| AlphaFold precedent (Tunstall) | MAMMAL como foundation model abierto para DTI |
| Lanes for AI vs humans (Tao) | Carril computacional (MAMMAL) + carril verificación (literatura auditada) |
| Chemistry competitions (Tao) | Futuras oportunidades de validación externa |

---

## Estado de nuestra pipeline vs el "loop ideal"

```
✅ HECHO:    16 targets verificados + 4 tiers
✅ HECHO:    DEGs GSE67311 analizados (señal mastocito)
✅ HECHO:    ESM2 embeddings (MOR outlier)
✅ HECHO:    MAMMAL DTI → pKd predictions (naltrexona→MOR: 6.91)
✅ HECHO:    Cross-predicciones (MS4A2 emerge como target off-label)
⏳ PENDIENTE: Cell-type annotation con MAMMAL (confirmar mastocito vs basófilo)
⏳ PENDIENTE: Arreglar Nav1.8 (secuencia > 1022 aa)
⏳ PENDIENTE: Validación externa (PDB docking, literatura adicional)
❌ FUTURO:   Wet-lab validation loop (requiere colaboración externa)
```

---

*Artefacto generado por DAVI desde transcripts del SAIR Science x AI Summit 2026*
*Repo: protein-lab/investigacion-fibromialgia/*
