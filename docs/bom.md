# Lista de materiales (BOM)

Precios consultados en octubre de 2026. "Final" = $→€ (BCE) + envío
Registered Post 16,09 € + 3 € arancel UE + 21 % IVA (cálculo en `pantallas-epaper.md`).

| # | Artículo | Dónde | Precio | Notas |
|---|---|---|---|---|
| 1 | **ESP32-S3-PhotoPainter con batería** (opción "3.7V Lithium battery: Included") | https://www.waveshare.com/esp32-s3-photopainter.htm | ~83,99 $ + 16,09 € envío → **113,79 €** final | **Recomendado.** Batería 3.7 V 1500 mAh con conector MX1.25 ya compatible. Solo ~1 $ más que sin batería. |
| 1b | ESP32-S3-PhotoPainter sin batería (SKU 32753) | https://www.waveshare.com/esp32-s3-photopainter.htm?sku=32753 | 82,99 $ + 16,09 € envío → **112,71 €** final | Solo si ya lo tienes o la batería con kit está agotada. |
| 1c | Mismo producto, distribuidor UE | https://eckstein-shop.de/waveshare-esp32-s3-photopainter-7-3inch-e6-fullcolor-epaper-frame_1 | ver web | Alemania, sin aduana. Comprobar si incluye batería. |
| 2 | Batería aparte (solo con 1b): LiPo 3.7 V, conector Molex PicoBlade / MX1.25 de 2 pines, con protección | Ej.: songyea 3000 mAh ×2, https://www.amazon.es/dp/B0FP5G3HHS (alternativas en `baterias.md`) | 16,99 € (×2) | 65×35×10 mm: comprobar que cabe. En Amazon.es no hay 1500 mAh con 1.25 mm. **Verificar polaridad**: pin 1 = +. |
| 3 | Cable USB-C ↔ USB-C (opcional) | cualquiera | ~5–10 € | El kit trae USB-A→USB-C; útil si el ordenador solo tiene USB-C. |
| — | Incluido en el kit | — | 0 | microSD 16 GB, lector, cable USB-A→C 1 m, altavoz 8 Ω, film, colgadores. |
| — | Ordenador siempre encendido | ya disponible | 0 | Servidor de la imagen y estación de programación. |

No hace falta: pila RTC de respaldo (https://www.waveshare.com/rtc-battery.htm); la hora la pone
el servidor en la imagen.

## Autonomía estimada
Cálculo teórico con 3 actualizaciones/día (6, 16 y 22 h):
- **Cada despertar ≈ 0,7 mAh:** arranque + WiFi + descarga de 192 KB (~5 s a ~110 mA ≈ 0,15 mAh) y
  refresco del panel (~25 s a ~50 mA ≈ 0,35 mAh), con margen. En total, ~2 mAh/día.
- **Deep sleep: es casi todo el gasto.** 1 mA (wiki) = 24 mAh/día; 2 mA (medido por usuarios en la
  Rev 1, `issues-photopainter.md`) = 48 mAh/día. La Rev 2 (ver `hardware.md`) debería consumir
  menos.
- **Capacidad útil ≈ 85 %** de la nominal (corte a ~3,3 V para el regulador, envejecimiento).

| Sleep | mAh/día | 1500 mAh (útil ~1275) | 3000 mAh (útil ~2550) |
|---|---|---|---|
| 2 mA | ~50 | ~3,5 semanas | **~7 semanas** |
| 1 mA | ~26 | ~7 semanas | **~14 semanas (~3 meses)** |
| 0,5 mA | ~14 | ~3 meses | ~6 meses |
| 0,3 mA | ~9 | ~4,5 meses | ~9 meses |

Con menos de ~0,3 mA el sleep deja de dominar y la autodescarga de la LiPo (~2–3 %/mes) empieza a
pesar.
