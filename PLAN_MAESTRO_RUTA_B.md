# Plan Maestro — Ruta B: Plataforma Bioelectroquímica Amplificada
## [Rol adoptado: Adam Heller — Biosensores electroquímicos e interconexión molecular directa]

## Diagnóstico del Estado Actual

El diseño original buscaba un "procesador bio-híbrido": ferritina + Au + MtrA/MtrF como computador. El MoE V1 dio 2/10. Los investigadores paralelos confirmaron:
- Au25/Au55 atómicamente preciso en ferritina = NO PUBLICADO
- Au8-Au12 = SÍ publicado (Comms Chem 5:39, 2022)
- NP policristalina Au(~2nm) = PUBLICADO (Ueno et al.)
- Cinética tunelamiento a ~12Å = lenta (k_ET decae exponencialmente)
- El concepto de "computación" con este sistema = fantasía dada la cinética
- El concepto de "amplificación/transferencia de electrones" = SÍ tiene precedentes publicados

## El Salto Conceptual: De Procesador → Plataforma Amplificadora

### La lección de Heller
Adam Heller (1933–2024) diseñó los primeros biosensores enzimáticos "wired" — electrodos con enzimas conectadas por cables moleculares redox. Su lección: no te preguntes "¿puede computar?" pregúntate "¿puede detectar/amplificar/señalar algo que no podía antes?"

### Analogía para Cristóbal
Imagina tu diseño original como querer hacer un microprocesador en tu garage. La Ruta B es: hagamos un amplificador de audio. No procesa bits individuales a GHz, pero SÍ transforma una señal microscópica en detectable por un multímetro, y eso SÍ puede patentarse/publicarse.

## La Arquitectura Ruta B (conservando todo lo bueno)

```
        ┌──────────────────────────────────────────────────────┐
        │           BIOCELDA ELECTROQUÍMICA                   │
        └──────────────────────────────────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    v               v               v
  ┌─────┐      ┌──────┐      ┌─────────┐
  │MtrA │───┐  │ Au   │      │MtrF     │
  │Hema │   ├──│ NP   │──────│Hema     │
  │     │───┘  │en    │      │         │
  └─────┘      │ferritin│     └─────────┘
               │(core) │
               └──────┘
                    │
                    v
             ┌─────────────┐
             │ Electrodos   │
             │ de trabajo   │
             │+ Referencia  │
             └─────────────┘
                    │
                    v
             ┌─────────────-─┐
             │  Señal de      │
             │  corriente     │
             │  (nA → μA)     │
             └─────────────────┘
```

### Qué cambia
| Componente | Diseño Original (Procesador) | Ruta B (Biosensor/Ampli) |
|-----------|------------------------------|--------------------------|
| Au55 cluster | Procesador central lógico | Nucleación site para ET|
| MtrA → Au → MtrF | Señal lógica | Circuito de ET medible |
| Velocidad objetivo | GHz (imposible) | ms-s (real con 12Å ET) |
| Métrica de éxito | Computación general | Amplificación detectable |
| Campo de publicación | Bio-computación (speculative) | Bioelectroquímica / Biosensores (establecido) |
| Precedente directo | Ninguno | Papers electrochem ferritina/SWNT publicados |

## Los Dos Modos de Operación Plausibles

### Modo 1: Sensor de Fe(II)/Fe(III) (menos ambicioso, más publicable)
- La ferritina ya almacena Fe como minerál core y tiene ferroxidasa center
- Au NP inyectado funciona como electrodos internos que aceleran el ingreso/egreso de electrones al core
- MtrA como puerta de entrada: captura electrones del electrode → inyecta en Au NP → desbloquea Fe del core → MtrF lleva electrones a la salida
- Lo que detectas: estado redox del hierro en el core
- Señal: cambio de conductancia de la celda
- Precedente: "Ferritin-Triggered Redox Cycling" ACS Anal Chem 2018 (citas reales verificadas)

### Modo 2: Amplificador de ET bacteriano (más ambicioso, pero plausible)
- Usar un SHE (Standard Hydrogen Electrode) modificado con monolayer de MtrA
- Ferritina-Au como "relay" (repetidor) molecular
- Aplicación: detector de respiración de Shewanella (biofuel cell monitoring)
- Precedente: "Direct electron transfer of ferritin" varios grupos ya lo estudian
- Lo que amplificas: el débil ET directo entre Shewanella y el electrodo

### Modo 3: Switcheable electrochemical cell (el más cool y real)
- El campo eléctrico ARG61/GLU- que descubrimos se convierte en un gate electrostático
- Al pH cambia (ARG=protonada ↩) el campo se invierte y el ET se desactiva
- Resultado: pH-gated electrochemical cell
- Precedente: gating enzimático por pH ya existe. Gating por campo interno de ferritina = NO publicado = paper potencial

## Precedentes Verificados (Tavily confirmados)

1. **Electrocatalytic ferritin/SWNT composite electrode** — publicado (Biosens Bioelectron 2011)
   - Ferritina + SWNT como mediadores de ET = REAL
2. **Ferritin-Triggered Redox Cycling** — ACS Anal Chem 2018
   - Redox cycling usando ferritina immobilizada en electrode = REAL
3. **Direct electron transfer of ferritin adsorbed on bare gold** — real, varios grupos
4. **Characterization of ferritin core on redox reactions as ET mediator** — Electrochim Acta 2010
5. **Au sub-nanocluster nucleation within ferritin** — Nat Comms 2017 (para partes mecano-estructurales)
6. **Au8-Au12 clustering in engineered ferritin** — Comms Chem 2022 (más reciente)

## Gap Real que Este Diseño Podría Llenar

**Gap identificado:** Nadie ha publicado una ferritina con TODOS estos elementos en simultáneo:
- Citocromos MtrA/MtrF wired a NP de oro interno
- CYS mutations neutral manteniendo cargas direccionales
- Caracterización electrochemica del sistema completo
- (Opcional) Gating de ET por estado redox del camp

## Plan de Fases

### Fase 1: In Silico (ahora)
- Modelar la interfaz MtrA-Au-ferritina usando PyMOL/ChimeraX
- Simulación de docking: ¿qué residuos de MtrA contactan el Au NP?
- Predicción de trayectoria ET a través del sistema (no necesitamos cinética de GHz, solo si hay path)
- Re-diseño del artefacto V3 → V4 (biosensor, no procesador)

### Fase 2: In Vitro (futuro, si tienes lab access)
- Expresión de 1BFR con mutaciones CYS en posiciones neutras (synthesis o company IDT)
- Reducción de Au3+ dentro del lumen → in situ Au NP formation
- Purificación con exclusion chromatography
- Monitoreo con TEM/UV-Vis/CD para verificar Au NP en lumen

### Fase 3: Electrochemistry (futuro)
- Immobilización en electrodo de carbono/carbon cloth
- Cyclic voltammetry con y sin ferritina-Au
- Medición de corriente anódica/cátódica vs. potencial
- Characterización de ET rate constants

### Fase 4: Integración con Shewanella (si quieres la estrella)
- Cultivo de S. oneidensis MR-1
- Célula electroquímica con electrodo-modificado bacteria
- Medición de current production correlacionado con presencia/ausencia de ferritin-Au

## Por Qué ESTA Ruta es Publicable (y la otra no)

| Criterio | Ruta A (Procesador) | Ruta B (Biosensor) |
|----------|---------------------|--------------------|
| Precedente directo | NINGUNO | SÍ, ferritina electrochem |
| Cinética plausible? | NO (GHz imposible) | SÍ (ms-s) |
| Síntesis Au posible? | NO (Au55 inestable) | SÍ (Au NP ~2nm publicado) |
| Quantifiable result? | NO (binario sin velocidad) | SÍ (μA de corriente) |
| Impacto científico | Hypothetical | Real y aplicable |
| Timeline a resultados | 5-10 años + millones | 1-3 años + colaborador con CV potentiostat |

## El Artefacto Rediseñado V4

Conservar del V3:
- 1BFR como chasis (NO cambiar)
- MtrA como puerta de entrada (conservar)
- 3-4 CYS en residuos neutros lumen-facing (conservar posiciones)
- ARG61+GLU44 preservados (conservar para gating opcional)

Eliminar del V3:
- Au55 (fantasía → reemplazar por Au NP policristalino ~2nm)
- Claims de "procesamiento" (→ "mediación de ET")
- "Velocidad de switch" como métrica de computación

Agregar:
- Electrodo de trabajo (glassy carbon, carbon cloth, o Au)
- Interfaz electrochem con medición de corriente
- Gate electroquímico (referencia Ag/AgCl)
- Señal medible: Δcurrent vs. potencial

## Reframing para Paper

**Título propuesto:**
> "Engineered Bacterioferritin-Gold Nanoparticle Hybrids as Modular Redox Mediators for Extracellular Electron Transfer Amplification"

**Abstract structure (paper real):**
1. Background: Shewanella ETR is slow; ferritin is robust but passive
2. Innovation: We create a ferritin-Au hybrid that actively mediates ET
3. Methods: CYS-engineered 1BFR + in situ Au NP nucleation + electrochemistry
4. Results: Quantifiable ET enhancement (numbers)
5. Conclusion: Bioelectrochemical amplifier platform

## Riesgos a Tener en Cuenta

1. **Au NP dentro de ferritina puede estar demasiado lejos del electrode.** Solución: ferritina immobilizada en electrodo (no en solución)
2. **MtrA no tiene afiniad natural por Au.** Solución: linker peptide o domain engineered con cysteinas de superficie
3. **Conductancia de Au NP ~2nm puede ser insuficiente.** Solución: verificar con conductancia conocida de Au clusters (~10^-5 S)
4. **ARG61/GLU44 gate puede no funcionar como tal.** Solución: gating electroquímico es bonus, no core

## Pregunta para Cristóbal

Te doy tres niveles de scope:

**Scope A (minimal):** Diseño in silico V4 + análisis de gaps. No más.

**Scope B (completo):** Diseño V4 + artefacto completo + paper outline + lista de colaboradores/lab que podría hacerlo real.

**Scope C (intermediate):** Scope A + integrar al menos una simulación numérica básica (por ejemplo: cálculo de tunneling rate con β=1.4 Å^-1 para la distancia real del sistema, demostrando que la señal es detectable).

¿Cuál scope quieres?
