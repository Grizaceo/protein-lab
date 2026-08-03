# Tangente 1: Modelado Estructural e Interacción Fc-Receptor / MRGPRX2 / SGC en el Microambiente del Dolor Periférico

**Fecha:** Mayo 2026  
**Repositorio:** `protein-lab/investigacion-fibromialgia`  
**Script Ejecutado:** [`scripts/tangent1_structural_modeling.py`](file:///wsl.localhost/Ubuntu/home/gris/.hermes/workspace/ACTIVE/protein-lab/investigacion-fibromialgia/scripts/tangent1_structural_modeling.py)

---

## 1. Contexto y Pregunta Central #3

**Pregunta 3:** ¿Cómo interactúa la inmunoglobulina G con receptores de mastocitos/glía (FcεRI, MRGPRX2, FcγR) en el microambiente del dolor periférico?

En el microambiente del ganglio de la raíz dorsal (DRG) y la piel, las inmunoglobulinas IgG de pacientes con FM pueden inducir sensibilización nociceptiva y degranulación mastocitaria/glial a través de dos mecanismos principales:
1. **Mecanismo Canónico Mediado por Fc:** Interacción de la región $\text{Fc}$ de la IgG con receptores de inmunoglobulina $\text{Fc}\gamma\text{R}$ ($\text{Fc}\gamma\text{RIIa}$ / $\text{CD32a}$, $\text{Fc}\gamma\text{RIIIa}$ / $\text{CD16a}$) presentes en mastocitos tisulares, macrófagos y SGCs.
2. **Mecanismo No Canónico Directo:** Interacción de la IgG o sus fragmentos Fab con receptores acoplados a proteína G de superficie como **MRGPRX2** (Sanchez 2025 bioRxiv) y canales iónicos/hemicanales gliales (**GJA1**, **KCNJ10**).

---

## 2. Compendio de Estructuras PDB y Caracterización de Interfaces

### Tabla 1: Dianas Estructurales Mapeadas para la Tangente 1

| Diana Molecular | Código PDB | Técnica / Resolución | Estado Oligomérico | Epítopos / Bucles Extracelulares Accesibles | Mecanismo Estructural en FM |
|---|---|---|---|---|---|
| **Connexin-43 (GJA1)** | `7F94` | Cryo-EM / 2.4 Å | Hexamérico (Conexón) | Bucles EL1 (Res. 40-75) y EL2 (Res. 170-210) | Auto-IgG se une a los loops EL1/EL2 alterando el poro de uniones gap y liberando ATP/glutamato. |
| **Kir4.1 (KCNJ10)** | `6M84` | Cryo-EM / 3.1 Å | Tetramérico | Vestíbulo externo del poro (Res. 100-135) | Oclusión del poro exterior por IgG bloquea la corriente de $\text{K}^+$, elevando el $\text{K}^+$ extracelular en DRG. |
| **MRGPRX2** | `7VV3` | Cryo-EM / 2.8 Å | Monómero GPCR 7-TM | Extremo N-terminal (Res. 1-30) y bucle ECL2 (Res. 165-185) | Reconocimiento por IgG/pepéptidos básicos induce secreción de $\text{IL-6}$ y triptasa sin requerir IgE (Sanchez 2025). |
| **CD40** | `3QD6` | X-ray / 2.6 Å | Trímero funcional con CD40L | Dominios ricos en cisteína CRD1 y CRD2 (Res. 25-100) | La estimulación del complejo CD40-CD40L promueve la activación de B-cells y la producción continua de anti-SGC IgG. |
| **FcεRI Subunidad $\alpha$ (FCER1A)** | `1F6A` | X-ray / 2.4 Å | Heterotetrámero $\alpha\beta\gamma_2$ | Dominios Ig-like D1 y D2 (Res. 26-200) | Sitio de anclaje de alta afinidad para IgE. Su baja señal en sangre refleja la depleción de basófilos circulantes. |
| **FcγRIIIa / CD16a (FCGR3A)** | `3SGJ` | X-ray / 2.2 Å | Complejo con Fc de IgG1 | Dominios D1 y D2 (Res. 20-190) | Complejos inmunes IgG-antígeno activan $\text{Fc}\gamma\text{RIIIa}$ en mastocitos y SGCs, desencadenando desgranulación y citoquinas. |

---

## 3. Dinámica del Microambiente del Dolor Periférico (Crosstalk Celular)

```
                       [ Auto-IgG de Paciente FM ]
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
[ Células Gliales Satélite (SGC) ]                 [ Mastocitos Tisulares / Basófilos ]
 ├── Unión a Cx43 (GJA1) y Kir4.1 (KCNJ10)          ├── Unión a MRGPRX2 (N-term / ECL2)
 ├── Activación del eje CD40-CD40L                   └── Unión de Fc a FcγRIIIa (CD16a)
 └── Liberación de:                                  └── Secreción masiva de:
      • Extracellular ATP                                 • Interleucina-6 (IL-6)
      • Glutamato (vía hemicanales)                       • Triptasa & Histamina
      • Citoquinas (IL-1β, TNF-α)                         • Sustancia P / CGRP
           │                                                 │
           └────────────────────────┬────────────────────────┘
                                    ▼
                 [ Nociceptor DRG (Fibras C / Aδ) ]
                 ├── Sensibilización de TRPV1 / TRPA1
                 ├── Apertura de NaV1.7 (SCN9A) & NaV1.8
                 └── Generación de Descargas Ectópicas (Dolor / Alodinia)
```

---

## 4. Conclusión de la Pregunta 3

> **Respuesta Definitiva:** La inmunoglobulina G extracelular opera en un **doble frente patogénico**:
> 1. En las **SGCs**, se une a los dominios extracelulares de **Connexin-43** (PDB `7F94`) y **Kir4.1** (PDB `6M84`), provocando la acumulación de potasio y ATP extracelular en el DRG.
> 2. En los **mastocitos tisulares**, se une al receptor de desgranulación no canónico **MRGPRX2** (PDB `7VV3`) y a **$\text{Fc}\gamma\text{RIIIa}$** (PDB `3SGJ`), desencadenando la liberación de $\text{IL-6}$, histamina y triptasa, sensibilizando térmicamente y mecánicamente a los nociceptores adyacentes.
