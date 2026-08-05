# Propuesta de Diseño: Lámina Teleprompter Autoalimentada de Reflectividad Selectiva

Este documento detalla el diseño conceptual de una **lámina inteligente activa retroajustable (ad-hoc)** para espejos. Está pensada bajo los principios de la ciencia de materiales avanzados, resolviendo la reflectividad, la transparencia selectiva, la captación de energía ambiental y la integración en un marco físico de borde discreto.

---

## 📐 Arquitectura del Sistema (Capas del Material)

Para lograr el efecto de letras flotantes en un espejo existente sin usar cables de alimentación gruesos, la lámina se compone de un compuesto multicapa nanoestructurado:

```
[Frente: Usuario]
  │
  ├── Capa 1: Espejo Dieléctrico (Reflexión selectiva de luz visible)
  ├── Capa 2: Matriz Transparente Activa (Cristal Líquido Colestérico / Electrocrómico)
  ├── Capa 3: Guía de Onda LSC (Concentrador Solar Luminiscente - Captación UV/IR)
  │
[Atrás: Espejo físico del usuario]
```

### 1. Reflectividad y Transparencia (Espejo Dieléctrico / Dicroico)
En lugar de un espejo metálico común (que bloquea la luz), la capa exterior utiliza un **Espejo Dieléctrico de película delgada**.
*   **Física**: Consiste en capas alternas de materiales con diferentes índices de refracción (como dióxido de titanio y dióxido de silicio). 
*   **Función**: Está sintonizado para reflejar la luz visible del entorno (actuando como espejo para el usuario) pero permitiendo que las longitudes de onda no visibles (infrarrojo y ultravioleta) pasen hacia las capas internas de captación de energía. Asimismo, permite el paso de la luz emitida por los caracteres del teleprompter desde el interior.

### 2. Matriz Transparente Activa (Emisión / Modulación de las Letras)
Para dibujar las letras consumiendo el mínimo de energía posible, se proponen dos tecnologías ad-hoc:
*   **Cristal Líquido Colestérico Transparente (ChLCD)**:
    *   *Ventaja*: Es una tecnología **biestable**. Esto significa que solo consume energía cuando el texto cambia de estado (es decir, cuando pasa a la siguiente línea de la letra). Mantener el texto estático en pantalla consume exactamente **0 vatios**.
    *   *Efecto*: Cuando el píxel está activo, refleja luz verde/amarilla brillante (aprovechando la luz ambiental); cuando está inactivo, es 100% transparente, dejando ver el espejo de fondo.
*   **Película Electrocrómica Segmentada**:
    *   Cambia de color (de transparente a oscuro/reflejante) mediante una reacción química reversible de transferencia de carga al aplicar un pulso de microvoltios.

### 3. Captación de Energía (Concentrador Solar Luminiscente - LSC)
El cuerpo principal de la lámina funciona como un colector solar transparente:
*   **Funcionamiento**: La lámina de polímero transparente está dopada con **puntos cuánticos (Quantum Dots)** o colorantes orgánicos luminiscentes.
*   **Captación**: Estos dopantes absorben la luz solar ultravioleta (UV) y la luz ambiental infrarroja (IR) sin obstruir la luz visible (manteniendo la transparencia del espejo).
*   **Efecto Guía de Onda**: La luz absorbida es re-emitida en una longitud de onda diferente y queda atrapada dentro del plástico por "reflexión interna total", viajando lateralmente hacia los bordes de la lámina.

---

## 🛠️ La "Baranda Sólida" de Borde (Hardware y Soporte)

Para evitar cableados invasivos, todo el hardware de control y conversión de energía se integra en una **baranda sólida perimetral** (perfil de aluminio o plástico extruido) que actúa como pinza de sujeción al borde del espejo.

```
       [ Baranda Sólida de Borde ]
      ┌───────────────────────────┐
      │  [ Celdas FV de Borde ]   │ ◄── Reciben la luz concentrada del LSC
      │  [ Micro-Batería / LiPo ] │ ◄── Almacena la energía recolectada
      │  [ Chip Wi-Fi (Ultra-LP) ]│ ◄── Recibe la letra desde la PC/Celular
      │  [ Driver del Display ]   │ ◄── Envía pulsos de voltaje a la pantalla
      └─────────────┬─────────────┘
                    │
           [ Lámina Activa ]
```

### Componentes de la Baranda:
1.  **Celdas Fotovoltaicas de Borde (Micro PVs)**:
    *   Tiras delgadas y altamente eficientes de arseniuro de galio (GaAs) o silicio cristalino ocultas dentro de la baranda. Reciben la luz concentrada que viaja por el borde de la lámina LSC y la convierten en energía eléctrica.
2.  **Sistema de Almacenamiento de Energía**:
    *   Una batería delgada de iones de litio (tipo moneda o tira flexible) o un **supercondensador** integrado en la baranda. Se recarga constantemente con la luz del día o la iluminación de la habitación.
3.  **Comunicaciones Ultra Bajo Consumo (Wi-Fi / BLE)**:
    *   Un microcontrolador integrado de baja potencia (ej. **ESP32-C6** o **nRF52840**). Utiliza protocolos de bajo consumo (como Wi-Fi 6 Target Wake Time o Bluetooth LE) para permanecer en modo de suspensión profunda (*deep sleep*). Solo se despierta cuando el servidor de `Singevery` envía los paquetes de texto de la canción activa.
4.  **Pinza Mecánica Discreta**:
    *   La baranda funciona como un clip de presión que abraza el borde del espejo del usuario, manteniendo la lámina tensa y estéticamente limpia, ocultando el pequeño transformador/cargador de respaldo para corriente si la energía solar no es suficiente.

---

## 📋 Ventajas del Diseño Ad-Hoc

*   **Retroajustable (Retrofit)**: Se instala sobre cualquier espejo estándar que el usuario ya tenga colgado.
*   **Autónoma (Self-Powered)**: Reduce o elimina la necesidad de cables colgantes gracias a la recolección de energía luminosa ambiental diaria (LSC + OPV).
*   **Invisible en Reposo**: Cuando no hay música sonando, el sistema permanece transparente y el espejo conserva su función reflectante original sin distorsiones.
