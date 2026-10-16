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
1500 mAh, 4 actualizaciones/día: con ≤1 mA en sleep (wiki) ~30 mAh/día → 6–7 semanas; con los
**~2 mA medidos por usuarios en la Rev 1** (`issues-photopainter.md`) ~55 mAh/día → **~4 semanas**.
La Rev 2 (ver `hardware.md`) debería consumir menos.

Con una batería de 3000 mAh: ~14 semanas a 30 mAh/día y ~8 semanas a 55 mAh/día.
