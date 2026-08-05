# Grounding: Extensión de Overlay de Juegos para PlayStation

Este documento analiza la viabilidad técnica y las limitaciones de crear una **extensión de overlay de juegos** para consolas PlayStation, comparando el enfoque de software (en la consola) versus el de hardware (en el espejo inteligente).

---

## 🔍 Interpretación 1: El Espejo como Pantalla de "Overlay Físico" del Juego

En este enfoque, el espejo actúa como una pantalla secundaria física colocada al lado del televisor. Mientras juegas en la PlayStation, la interfaz del juego (HUD, minimapa, inventario, telemetría o chat de Twitch/Discord) se desplaza al espejo, dejando la pantalla del televisor limpia e inmersiva.

### Viabilidad Técnica:
*   **En consolas (PS5/PS4)**: Sony no permite que las aplicaciones se comuniquen libremente entre sí dentro de la consola por motivos de seguridad (sandboxing).
*   **La Solución (Protocolo UDP/APIs)**: Varios juegos populares de PlayStation transmiten datos de telemetría y estado del juego en tiempo real a través de la red local mediante paquetes **UDP**.
    *   *Ejemplo (Gran Turismo 7, F1 2026, Project CARS)*: Envían velocidad, marcha, tiempos de vuelta y estado del coche al puerto UDP `33740` o `20777`. El chip de la baranda del espejo puede escuchar este puerto directamente en la red local y renderizar un velocímetro y cuentarrevoluciones flotando sobre el espejo en tiempo real.
    *   *Ejemplo (Otros juegos con Companion Apps)*: Algunos juegos exponen APIs web locales. Un servidor intermediario en la PC (o la misma app de Singevery) puede capturar estos datos y enviarlos al espejo.
    *   *Chat de streaming*: Si el usuario transmite en Twitch o Discord desde la consola, la app de Singevery lee el chat mediante la API de Twitch y lo muestra en el espejo para que el jugador lea el chat sin tapar la pantalla del juego.

---

## 🔍 Interpretación 2: Una App de "Overlay de Software" en PlayStation (Sobre la TV)

En este enfoque, el usuario descarga una extensión desde la PlayStation Store que dibuja un recuadro translúcido (con letras de canciones, chat de Discord o estadísticas) **encima del propio juego en el televisor** (similar a Discord Overlay en PC).

### Limitaciones del Sistema Operativo de PlayStation (Sony OS):
*   **Sistema Cerrado**: Sony **no permite** que desarrolladores independientes publiquen aplicaciones que dibujen capas gráficas (*overlays*) encima de otros juegos comerciales en ejecución. Las únicas apps que pueden hacer esto son las del propio sistema operativo de Sony (como el reproductor de Spotify oficial, el chat de grupo de PlayStation Party en modo Picture-in-Picture, o las tarjetas de actividad del Centro de Control).
*   **La Vía del Streaming (Twitch Extensions)**:
    *   Si el usuario transmite su juego de PlayStation a Twitch, se puede crear una **Twitch Extension**. El overlay con la letra de la canción se renderiza sobre el reproductor de Twitch para los espectadores, pero el jugador no lo verá en su TV mientras juega directamente, a menos que tenga el stream abierto al lado.
*   **La Vía del Hardware de Intermediación (HDMI Overlay Box)**:
    *   Para inyectar un overlay físico en la TV de la consola sin alterar el software de Sony, se requeriría una pequeña caja de captura/paso HDMI (tipo *HDMI Overlay Box* o *Capture Card* conectada a un mini PC/Raspberry Pi) que mezcle la señal de video de la consola con la de la app de teleprompter antes de enviarla a la TV. Esto encarece el producto.

---

## 📋 Conclusión de Viabilidad

| Enfoque | Viabilidad Técnica | Dificultad | Experiencia de Usuario |
| :--- | :--- | :--- | :--- |
| **Espejo como HUD / Telemetría Física** (UDP en red local) | **Alta (100% Viable)** | Media | Excelente (Pantalla de TV limpia + datos flotando en el espejo del setup). |
| **App de Overlay en Consola** (PlayStation Store sobre la TV) | **Nula (Bloqueado por Sony)** | Imposible | No disponible para desarrolladores independientes en el OS de PS5. |
| **Overlay para Espectadores** (Twitch Extension / OBS) | **Alta** | Baja-Media | Excelente para creadores de contenido/streamers que cantan o juegan. |
