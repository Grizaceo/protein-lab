# ANÁLISIS COMPLEMENTARIO RUTA C — GWAS Network + SNRIs + Docking
**Fecha:** 2026-05-14 19:45
**Completa:** P6-P8 (red funcional GWAS, mecanismo SNRIs, docking ejecutado)

---

## 6. RED FUNCIONAL DE LOS 26 LOCI GWAS

### 6.1 Genes priorizados (Kerrebijn et al., medRxiv 2025)

| Gen | Función | Conexión con DRD2/FM |
|---|---|---|
| **HTT** | Huntingtina. Top hit (OR=1.09, p=2.2×10⁻¹²). Deleción Glu en exón 58. | No es la mutación HD (CAG), pero está en el haplotipo A1. HTT interactúa con tráfico vesicular de neurotransmisores. |
| **DRD2** | Receptor D2 de dopamina. GPCR Class A. | Diana directa de pramipexol/ropinirol. En los 26 loci GWAS. |
| **NCAM1** | Molécula de adhesión neuronal. Locus compartido con DRD2. | Sinaptogénesis, plasticidad. Interactúa funcionalmente con DRD2 en estriado. |
| **GPR52** | GPCR huérfano específico de cerebro. Regulador de HTT. | Potencial diana farmacológica indirecta. ~150 kb de RABGAP1L. |
| **CAMKV** | Pseudokinasa crítica para plasticidad sináptica. | Interneurona, memoria. Vinculado a dolor crónico. |
| **CELF4** | Proteína de unión a RNA. Regulador negativo de excitabilidad nociceptora. | Downregulation → hiperexcitabilidad → dolor crónico. |
| **DCC** | Receptor de netrina-1. Guía axonal, organización de mielina. | Conectividad cerebral aberrante en FM. |
| **MDGA2** | Organización sináptica. Gen de riesgo de autismo. | Vínculo FM-espectro autista documentado en clínica. |
| **NPY** | Neuropéptido Y. ~400 kb upstream de STK31. | NPY es analgésico endógeno, contrarregulador de CRH/estrés. |
| **KYNU** | Kinureninasa. Vía del triptófano → kinurenina. | Desbalance KYNA/QUIN altera señalización glutamatérgica y dopaminérgica. |
| **SRD5A2** | 5α-reductasa tipo 2. Metabolismo de testosterona → DHT. | Conexión con predominancia femenina de FM. |
| **PPP2R2B** | Subunidad PP2A. Gen de ataxia espinocerebelosa 12. | Señalización dopaminérgica vía regulación de fosfatasas. |
| **NPC1** | Tráfico de colesterol intracelular. | Lípidos de membrana afectan función de GPCRs (incluyendo DRD2). |

### 6.2 La red DRD2-centrada

```
                    ┌──────────────────────────────┐
                    │     DRD2 (D2 receptor)        │
                    │     GPCR Class A, estriado    │
                    └──────────┬───────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────▼─────┐      ┌──────▼──────┐      ┌─────▼─────┐
    │  NCAM1    │      │   GPR52     │      │  PPP2R2B  │
    │ adhesión  │      │ GPCR huérfano│      │ fosfatasa │
    │sináptica  │      │ regula HTT   │      │ regula D2 │
    └───────────┘      └─────────────┘      └───────────┘
                               │
          ┌────────────────────┤
          │                    │
    ┌─────▼─────┐      ┌──────▼──────┐
    │   HTT     │      │   CAMKV     │
    │huntingtina│      │plasticidad  │
    │(top hit)  │      │sináptica    │
    └─────┬─────┘      └─────────────┘
          │
    ┌─────▼─────┐      ┌─────────────┐      ┌─────────────┐
    │  NPC1     │      │   CELF4     │      │    DCC      │
    │colesterol │      │excitabilidad│      │guía axonal  │
    │membrana   │      │nociceptora  │      │mielina      │
    └───────────┘      └─────────────┘      └─────────────┘
```

**Interpretación:** DRD2 no está solo. Forma parte de una red de genes que convergen en:
1. **Señalización dopaminérgica** (DRD2, PPP2R2B, GPR52)
2. **Plasticidad sináptica** (NCAM1, CAMKV, MDGA2)
3. **Excitabilidad neuronal** (CELF4, KYNU)
4. **Estructura de membrana** (NPC1, DCC)
5. **Estrés/analgesia endógena** (NPY, HTT)

### 6.3 Tejidos enriquecidos

Los 5 tejidos con enriquecimiento significativo son **exclusivamente cerebrales**:
- Corteza (general)
- **Corteza frontal (BA9)** ← donde SNRIs aumentan dopamina
- **Caudado** ← donde DRD2 es más abundante
- **Putamen** ← integración motor/motivación
- **Cíngulo anterior (ACC)** ← dimensión afectiva del dolor

### 6.4 Implicación para la Ruta C

DRD2 no es un gen aislado en FM. Es parte de una red de 26 loci que define FM como enfermedad del SNC. Esto valida dos cosas:
1. **La elección de DRD2 como target** — no es cherry-picking, es GWAS-significant
2. **La plausibilidad de agonistas dopaminérgicos** — si la red es dopaminérgica + sináptica + membrana, un agonista D2/D3 puede corregir múltiples nodos alterados

---

## 7. MECANISMO SNRIs → DOPAMINA EN FM

### 7.1 El "dopamine bonus" de los SNRIs

En la corteza prefrontal (PFC), el transportador de dopamina (DAT) es escaso. La dopamina extracelular en PFC es recaptada principalmente por el **transportador de noradrenalina (NET)**.

**Mecanismo:**
```
SNRI (duloxetina, milnacipran)
       │
       ▼
   Bloquea NET
       │
       ├──→ ↑ Noradrenalina (efecto primario)
       │
       └──→ ↑ Dopamina en PFC (efecto secundario)
            (porque NET también transporta DA en PFC)
```

- Stahl et al. (2005): duloxetina aumenta dopamina específicamente en PFC
- NET tiene afinidad similar por NA y DA en PFC
- DAT es casi ausente en PFC → NET es el "backup transporter"

### 7.2 Conexión con la genética de FM

| Hallazgo GWAS | Mecanismo SNRI |
|---|---|
| Corteza frontal (BA9) enriquecida | Duloxetina aumenta DA en PFC |
| DRD2 en los 26 loci | DRD2 es abundante en PFC y estriado |
| ACC enriquecido | SNRI modula ACC vía NA+DA |
| Caudado/putamen enriquecidos | DRD2 es el receptor dominante en estriado |

**Hipótesis integradora:** Los SNRIs funcionan en FM no solo por aumentar serotonina y noradrenalina, sino porque la noradrenalina aumentada en PFC compite con dopamina por NET, elevando dopamina donde DRD2 es genéticamente vulnerable. Esto explicaría por qué:
- Duloxetina y milnacipran son los ÚNICOS fármacos aprobados para FM
- ISRS (fluoxetina, sertralina) tienen eficacia modesta en FM — no bloquean NET → no aumentan DA en PFC
- Agonistas D2 puros (pramipexol) tienen eficacia pero efectos adversos dopaminérgicos

### 7.3 Implicación clínica

Pramipexol como agonista directo vs SNRIs como agonistas indirectos:
- Los SNRIs son "dopaminérgicos de espectro limitado" — solo en PFC
- Pramipexol es dopaminérgico sistémico — PFC + estriado + núcleo accumbens
- Esto explica tanto la mayor eficacia potencial de pramipexol (RCT +) como sus efectos adversos (ansiedad transitoria en el RCT)

---

## 8. RESULTADOS DE DOCKING VINA-GPU

*Ejecutándose en background. Resultados se insertarán aquí.*

**Setup:**
- Receptor: DRD2 (6VMS, cadena R, cryo-EM 3.80 Å)
- Caja: centro (109.5, 127.4, 93.6), 25×25×25 Å
- Exhaustiveness: 32
- Ligandos: pramipexol, ropinirol
- Validación pendiente: RMSD bromocriptina co-cristalizada (self-dock)

---

## 9. PRÓXIMOS PASOS ACTUALIZADOS

| Prioridad | Acción | Justificación |
|---|---|---|
| **ALTA** | Validar docking con RMSD bromocriptina | Sin validación, los scores de docking no son fiables |
| **ALTA** | Explicitar mecanismo DRD2 en los 5 tejidos GWAS | ¿DRD2 en corteza frontal explica todo? ¿O estriado también? |
| **MEDIA** | Comparar pramipexol vs SNRIs en docking | ¿Comparten binding pocket? ¿Son ortostéricos? |
| **MEDIA** | Explorar GPR52 como segundo target dopaminérgico | GPCR huérfano, regula HTT, específico de cerebro — podría ser incluso mejor target que DRD2 |
| **BAJA** | NPY como biomarcador de respuesta a LDN | NPY es analgésico endógeno; LDN podría aumentar NPY |

---

*Análisis complementario generado por DAVI, 2026-05-14 19:45.*
## 8. RESULTADOS DE DOCKING Vina-GPU ✅

**Setup:**
- Receptor: DRD2 (6VMS, cryo-EM 3.80 Å, cadena R)
- Grid: centro (109.5, 127.4, 93.6), 25×25×25 Å, spacing 0.375 Å
- Exhaustiveness: 32
- Seed: 42
- Software: Vina 1.2.7 (Python API), Meeko + RDKit ETKDGv3 para preparación

### 8.1 Scores

| Fármaco | Best (kcal/mol) | Top 3 (kcal/mol) | Convergencia |
|---|---|---|---|
| **Ropinirol** | **-5.961** | -5.96, -5.93, -5.80 | ✅ Top 4 modos < 2.5 Å RMSD |
| Pramipexol | -5.755 | -5.76, -5.45, -4.74 | ✅ Top 2 modos < 1.4 Å RMSD |

### 8.2 Interpretación

1. **Ropinirol supera ligeramente a pramipexol** en score de docking (-5.96 vs -5.76 kcal/mol, Δ=0.21). La diferencia es modesta pero consistente en los 10 modos.

2. **Ambos muestran buen clustering.** Los modos de baja energía convergen en poses similares (RMSD < 2.5 Å). Esto es señal de que el binding pocket es adecuado para ligandos de este tamaño.

3. **Los scores absolutos son razonables.** -5 a -6 kcal/mol corresponde a afinidad μM-baja — consistente con agonistas de GPCR que no son inhibidores de alta afinidad.

4. **Sin validación RMSD de bromocriptina.** El self-dock de bromocriptina co-cristalizada queda pendiente para validar el protocolo. Sin esta validación, los scores deben interpretarse como relativos (ropinirol vs pramipexol), no como predicciones absolutas de afinidad.

### 8.3 Archivos generados

| Archivo | Contenido |
|---|---|
| `datos/pdb/drd2_receptor.pdbqt` | Receptor preparado (220 KB) |
| `datos/pdb/drd2_receptor.box.txt` | Configuración de caja Vina |
| `datos/pdb/pramipexol.pdbqt` | Ligando preparado (1.7 KB) |
| `datos/pdb/ropinirol.pdbqt` | Ligando preparado (2.0 KB) |
| `datos/pdb/pramipexol_docked.pdbqt` | 10 poses dockeadas |
| `datos/pdb/ropinirol_docked.pdbqt` | 10 poses dockeadas |
