# Pantallas e-paper

Catálogo de pantallas candidatas, ordenado por precio final.

**Precio final** = lo que pagarías en España:
- Tiendas fuera de la UE (Waveshare y Good Display envían desde China): precio en $ convertido a €
  (BCE 2026-10-09: 1 € = 1,1206 $) + envío + **3 € de arancel** (tasa fija de la UE para paquetes de
  ≤150 €, en vigor del 1-7-2026 a julio 2028) + **21 % IVA** sobre todo (el envío también paga IVA).
  Waveshare: incluye el envío más barato (16,09 €, ver notas). Good Display: **sin envío** (no
  consultado). No incluye la posible tarifa de gestión de la paquetería.
- Pimoroni (tienda EU): IVA y aranceles ya incluidos ("nothing more is due on delivery"). El precio
  se consultó con región Austria (IVA 20 %); en España (21 %) puede variar unos céntimos.

"6 (Spectra 6)" = negro, blanco, rojo, amarillo, azul y verde.

| Nombre | Tamaño | Colores | WiFi | Batería | Precio | Precio final (España) | Última actualización | Link |
|---|---|---|---|---|---|---|---|---|
| Pimoroni Inky Impression (PIM789) | 4.0" · 600×400 | 6 (Spectra 6) | No (la pone la Raspberry Pi) | No | 39,95 € (antes 49,95 €) | **39,95 €** | 2026-10-12 | https://shop.pimoroni.com/en-eu/products/inky-impression?variant=56039376912763 |
| Good Display GDP075FU1 (solo USB, liquidación) | 7.5" · 800×480 | 4 (negro, blanco, rojo, amarillo) | No | No | 51,89 $ | **59,66 €** | 2026-10-12 | https://www.buy-lcd.com/products/gdp075fu1?VariantsId=11240 |
| Pimoroni Inky Impression (PIM773) | 7.3" · 800×480 | 6 (Spectra 6) | No (la pone la Raspberry Pi) | No | 63,95 € (antes 79,95 €) | **63,95 €** | 2026-10-12 | https://shop.pimoroni.com/en-eu/products/inky-impression?variant=55186435244411 |
| Good Display GDP075FW1 (WiFi, USB) | 7.5" · 800×480 | 4 (negro, blanco, rojo, amarillo) | Sí | No (USB) | 57,89 $ | **66,14 €** | 2026-10-12 | https://www.buy-lcd.com/products/gdp075fu1?VariantsId=11240 |
| Good Display GDP075FW1B (batería 4000 mAh, WiFi, MQTT) | 7.5" · 800×480 | 4 (negro, blanco, rojo, amarillo) | Sí | Sí, 4000 mAh | 62,90 $ | **71,55 €** | 2026-10-12 | https://www.buy-lcd.com/products/gdp075fu1?VariantsId=11240 |
| Waveshare ESP32-S3-PhotoPainter (sin batería, SKU 32753) | 7.3" · 800×480 | 6 (Spectra 6) | Sí | Conector MX1.25, no incluida | 82,99 $ + 16,09 € envío | **112,71 €** | 2026-10-12 | https://www.waveshare.com/esp32-s3-photopainter.htm?sku=32753 |
| Waveshare ESP32-S3-PhotoPainter (con batería 1500 mAh) | 7.3" · 800×480 | 6 (Spectra 6) | Sí | Sí, 1500 mAh | ~83,99 $ + 16,09 € envío | **113,79 €** | 2026-10-12 | https://www.waveshare.com/esp32-s3-photopainter.htm |
| Pimoroni Inky Impression (PIM774) | 13.3" · 1600×1200 | 6 (Spectra 6) | No (la pone la Raspberry Pi) | No | 184,95 € (antes 230,95 €) | **184,95 €** | 2026-10-12 | https://shop.pimoroni.com/en-eu/products/inky-impression?variant=55186435277179 |

## Notas

### Waveshare ESP32-S3-PhotoPainter (la que usa este proyecto)
- 800×480, E Ink Spectra 6, refresco ~25 s. ESP32-S3 integrado con WiFi, PMIC AXP2101,
  conector de batería, marco de madera. Funciona sola, sin ordenador. Ver `bom.md` y `hardware.md`.
- El precio en $ es el de la web de Waveshare; envía desde China.
- Envío a España (checkout, 2026-10-12, "Weight Based Shipping"): Registered Post Air Mail 16,09 €
  (12–28 días) · Yanwen 16,09 € (12–30 días) · DHL 34,42 € (9–12 días) · FedEx 35,20 € (9–12 días) ·
  UPS 73,30 € (12–15 días). El precio final usa 16,09 €; con DHL sería 134,89 € / 135,97 €
  (sin / con batería), y los couriers suelen cobrar además gestión aduanera.

### Pimoroni Inky Impression
- E Ink Spectra 6. 4.0": 600×400, refresco 12 s. 7.3": 800×480, 28 s (paneles desde abril
  2026 con forma de onda "AC": mejores colores, algo más lenta). 13.3": 1600×1200, 12 s.
- **Es una placa HAT para Raspberry Pi**: no lleva microcontrolador ni WiFi; se controla por
  SPI desde una Raspberry Pi (Zero incluida) con la librería Python `pimoroni/inky`.
  No menciona soporte de batería. Para este proyecto haría falta además una Pi y su alimentación.
- 4 botones traseros, conectores Qw/ST (I2C), sin marco (la 7.3" cabe en un marco Ikea de 180×130 mm).
- Precios de la tienda EU con IVA y aranceles incluidos; estaban en oferta (-20 %) el 2026-10-12.
- Guía: https://learn.pimoroni.com/article/getting-started-with-inky-impression
- Esquemático 7.3": https://cdn.shopify.com/s/files/1/0174/1800/files/inky_impression_73_spectra_schematic.pdf?v=1745854872

### Good Display GDP075F (buy-lcd.com)
- Etiqueta de precio / cartel e-paper con carcasa (196×138×12 mm) y controlador incluido; no es un
  panel suelto. Panel GDEM075F52, 4 colores, refresco ~20 s. Las tres versiones están en la misma
  página (selector "Product").
- **GDP075FW1B**: ESP32-WROOM-32D, batería Li-ion 4000 mAh recargable, WiFi + MQTT, sleep
  configurable 1–24 h. Software ImageToWiFi + MQTT2EPD. La más parecida a este proyecto.
- **GDP075FW1**: ESP32-WROOM-32D, WiFi, alimentación USB continua.
- **GDP075FU1**: STM32F1, solo Micro USB (driver CH340, software ImageToUSB), sin WiFi.
- Precios en USD por variante (datos de la página); un banner anunciaba -15 % que podría no estar
  reflejado. Stock el 2026-10-12: 19 / 14 / 19 unidades.
