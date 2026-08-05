# Análisis de Producto, Mercado y Viabilidad Financiera: Kit Espejo-Teleprompter

Este informe presenta el análisis comercial, logístico y financiero para el lanzamiento del **Kit Espejo-Teleprompter (Singevery)**, incluyendo la viabilidad de la integración con la PlayStation Store y el desglose de costos de transacción internacionales.

---

## 1. Análisis de Producto y Mercado

### Propuesta de Valor Única (USP)
Un **kit de adaptación (retrofit)** de bajo coste que convierte cualquier espejo común en un teleprompter de karaoke inalámbrico autoalimentado, sincronizado en tiempo real con lo que suena en el entorno (PC, móvil, consola).

### Público Objetivo (Target)
1.  **Entusiastas del Karaoke y la Música**: Personas que disfrutan cantando en casa pero no quieren tener una pantalla gigante interrumpiendo la estética de su habitación o baño.
2.  **Gamers (Consola/PlayStation)**: Jugadores de títulos de karaoke (como *Let's Sing* o *SingStar*) y usuarios de Spotify/Apple Music en consolas.
3.  **Hogares Inteligentes (Smart Home)**: Clientes que buscan tecnología estética y "oculta" (*ambient computing*).

### La Conexión PlayStation (Oportunidad de Mercado)
Lanzar una extensión/app en la **PlayStation Store** representa una ventaja competitiva masiva:
*   **Integración**: La consola PS5/PS4 ejecuta la app de Singevery en segundo plano (o como app compañera). Al reproducir música en Spotify de la PS5 o al jugar un juego de canto, la app de PlayStation captura los metadatos o el audio y los transmite por la red local (Wi-Fi local vía WebSockets/UDP) a la baranda del espejo.
*   **Mercado Gamer**: Los gamers de consola representan un nicho dispuesto a pagar por accesorios de hardware complementarios (kits de luces, cámaras, auriculares, etc.).

---

## 2. Estructura de Costos de Transacción y Logística (Lote de 1,000 unidades)

Para importar el producto desde Shenzhen (China) y distribuirlo en América Latina (ej. Chile) o Norteamérica/Europa, se deben considerar los siguientes costos adicionales sobre el costo de fabricación (BOM de ~$19.00 USD):

### A. Costos de Transporte e Importación (Unitario)
*   **Flete Marítimo (LCL consolidado) + Seguro**: ~$1,500 USD por pallet (caben las 1,000 unidades en caja compacta).
    *   *Costo unitario flete*: **$1.50 USD**
*   **Derechos de Aduana / Arancel de Importación**: Típicamente entre 4% y 6% sobre el valor FOB bajo código arancelario HS 8528.59 (pantallas planas).
    *   *Arancel unitario (6% de $19.00)*: **$1.14 USD**
*   **Gastos de Despachador de Aduana y Puerto**: Honorarios y almacenaje.
    *   *Costo unitario*: **$0.80 USD**
*   **Costo de Internación Total (Landded Cost)**: **$22.44 USD** (Costo en bodega de destino).

### B. Costos de Transacción y Operación de Venta (Unitario)
*   **Comisión Pasarela de Pago (Stripe/Shopify Pay)**: ~3% + $0.30 USD sobre el precio de venta.
    *   *Asumiendo PVP de $69.00 USD*: **$2.37 USD**
*   **Almacenamiento y Envío al Cliente (3PL / Fulfillment)**: Almacén externo que recibe el pedido, empaca y envía.
    *   *Tarifa plana de empaque y envío doméstico*: **$6.50 USD**
*   **Impuestos Locales (IVA / Sales Tax)**: En Chile el IVA es del 19%. En venta directa (D2C) internacional, se puede estructurar para que el IVA sea pagado por el cliente en aduana de destino o incluirlo en el precio final.
    *   *Si se incluye en el precio final de $69 USD (19% IVA)*: **$11.01 USD**

---

## 3. Matriz Financiera y Margen Neto (Escenario D2C)

Asumiendo un precio de venta al público (PVP) de **$69.00 USD** (con impuestos incluidos en destino, ej. Chile/Latam):

```
[ PVP: $69.00 USD ]
   ├── IVA/Impuesto local (19%): $11.01 USD (Neto: $57.99 USD)
   ├── Costo del Producto en Bodega (Landed): $22.44 USD
   ├── Comisión Pasarela (Stripe): $2.37 USD
   ├── Fulfillment (Envío local): $6.50 USD
   └── Margen de Ganancia Neto: $26.68 USD
```

### Indicadores Financieros:
*   **Margen Bruto (sobre el producto neto)**: **61.3%**
*   **Margen Neto por Unidad**: **$26.68 USD** (38.6% del PVP total).
*   **Punto de Equilibrio (Break-Even)**: Con un lote de 1,000 unidades vendidas, el retorno neto neto es de **$26,680 USD**, recuperando la inversión inicial de fabricación (~$19,000 USD) en las primeras 413 unidades vendidas.

---

## 4. Viabilidad y Prospectos de Mercado

### Fortalezas del Proyecto:
1.  **Barrera de Entrada**: Requiere conocimiento tanto de software (app de sincronización) como de hardware físico (óptica de espejos). Esto evita clones rápidos de software puro.
2.  **Facilidad de Envío**: Al ser una lámina enrollable y una baranda delgada de aluminio de unos 40 cm, el paquete pesa menos de 300 gramos, lo que abarata drásticamente el flete internacional y el envío al cliente comparado con enviar espejos reales con vidrio grueso.

### Riesgos y Mitigación:
*   **Curva de aprendizaje del usuario**: Pegar una lámina sin burbujas puede molestar a algunos usuarios.
    *   *Mitigación*: Incluir en el kit un kit aplicador (espátula plástica + atomizador de agua jabonosa) y un video instructivo animado accesible por código QR.
*   **Licenciamiento de PlayStation Store**: Desarrollar para PlayStation requiere convertirse en partner oficial de Sony y pasar su proceso de certificación de seguridad de red.
    *   *Mitigación*: Lanzar primero la app compañera para móviles (Android/iOS) y PC. La app de PlayStation puede desarrollarse en una segunda fase utilizando WebGL/C++ nativo una vez el hardware esté validado en el mercado.
