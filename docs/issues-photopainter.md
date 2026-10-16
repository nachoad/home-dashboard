# Issues cerrados del repo oficial del PhotoPainter

Resumen de los issues cerrados de https://github.com/waveshareteam/ESP32-S3-PhotoPainter/issues?q=is%3Aissue+state%3Aclosed
(10 issues, consultados el 2026-10-12). Solo como referencia: lo que dicen los usuarios no está verificado.

## Lo más relevante para este proyecto

### Hay dos revisiones de placa
- **Rev 1:** PMIC **AXP2101**. Es la que describen el esquemático de la wiki. Notas de una Rev 2: `hardware.md`.
- **Rev 2:** PMIC marcado **TG28** (la página de producto ya lo menciona).
  - El **INT del RTC PCF85063 va al botón de encendido (PWRON) del PMIC**. Así el RTC puede encender la
    placa a una hora programada y el sistema puede apagarse del todo entre actualizaciones.
    Un usuario estimaba ~40 µA en ese modo.
  - Esquemático v2: https://www.waveshare.net/w/upload/a/ae/ESP32-S3-PhotoPainter-Schematic-v2.0.pdf
    (la wiki en inglés aún enlaza el v1).
  - Según un usuario al que se la cambiaron, desaparecen todos los problemas de alimentación de la Rev 1.
- **Al recibir la placa, comprobar qué revisión es** (serigrafía "REV2" o el chip TG28) antes de fiarse
  de los pines del PMIC y del RTC.

### Rev 1: reinicios con USB-C y batería a la vez (#5)
- Varios usuarios: con USB **y** batería conectados, el ESP32 se reinicia aleatoriamente (brownout).
  Pasa con cualquier firmware: el oficial, esp32-photoframe, ESPHome. Pasa más con la batería casi llena.
  Si solo hay USB o solo batería, no pasa.
- Otros síntomas: errores de I2C con el PMIC (el código oficial reintenta 3 veces), porcentaje de
  batería poco fiable (se apagó con 97 % mostrado) y carga lenta (<100 mA) con algunos cargadores.
- Workaround (@altugbakan): `axp.disableCellbatteryCharge()` mientras se usan la pantalla y el WiFi,
  y reactivar la carga después. Sospecha que R28 (0 Ω) debería ser un filtro RC.
- Waveshare: contactar con ventas o soporte para cambiar la placa por una Rev 2 (a algunos se la
  cambiaron y a otros les mandaron solo reflashear).
- **Para nuestro firmware:** con USB no dormimos, así que el caso USB + batería se dará al cargar. Hay
  que tenerlo en cuenta (o desactivar la carga durante la actualización).

### Consumo en deep sleep real: ~1,5–3 mA en Rev 1 (#1, #5)
- La wiki llegó a decir "<0,01 µA" y luego "≤1 mA". Medido por usuarios: **~2 mA** (desde USB).
  Un usuario con 1500 mAh y 1 actualización/día: pierde ~10 %/día y le dura **2–4 semanas**.
- Recomendaciones de Waveshare:
  1. Apagar LDOs innecesarios del AXP2101, luego poner el AXP2101 en sleep (con el pin de IRQ
     configurado para despertar) y por último el ESP32.
  2. Poner el SHTC3 en sleep.
  3. Desactivar la monitorización ADC del AXP2101 en sleep.
  - Código de referencia: `04_PowerConsumptionTest/01_Arduino_Src/01_Fac_Test`.
- **ALDO3 (audio) y el bus I2C:** el codec (ES8311/ES7210) cuelga del mismo I2C que el PMIC. Si se
  apaga ALDO3, al despertar el codec sin alimentar tira del I2C a masa y `axp2101.begin()` falla.
  - Waveshare: apagar ALDO3 **lo último** y dar más retardo al despertar. También dice que no hace
    falta apagar el codec, basta su modo de bajo consumo (2–3 mA más).
  - Usuario (@CrazyRangerBob): el I2C cruza los dominios `VCC_3V3` y `Audio_VCC`. Con el audio
    apagado, las pull-ups alimentan el codec por sus diodos de protección, así que no se llega a µA.
- No hay pistas que cortar para dejar solo ESP32 + pantalla. Waveshare: se podría bajar algo
  subiendo las resistencias pull-up.
- **Para estimar la autonomía:** en Rev 1, contar con ~2 mA en sleep (≈48 mAh/día solo
  durmiendo), no ≤1 mA.

### Pantalla
- **Hay que encender ALDO4 (3,3 V) del AXP2101** antes de usar el panel. Si no, el panel no reacciona (#1).
- Imagen "quemada"/lavada al arrancar con GxEPD2: Waveshare recomienda dejar el panel sin alimentar
  durante el arranque y encender ALDO4 solo para enviar datos y refrescar (#5).
- GxEPD2 tiene driver para este panel: `GxEPD2_730c_GDEP073E01` (6 colores, 800×480) (#5).
- Una franja parcial de la imagen en el modo 1 resultó ser la **microSD de fábrica defectuosa**
  (errores de E/S en el log). Con otra tarjeta, bien (#1).

### Timer de deep sleep (#6)
- Bug del firmware oficial: `esp_sleep_enable_timer_wakeup(basic_rtc_set_time * 1000 * 1000)` con
  `int` desborda a partir de ~35 min (21600 s acababa en ~2 min). Hay que usar
  `(uint64_t)segundos * 1000000ULL`. Nuestro `main.cpp` ya lo hace así; vigilarlo en cambios.
- El firmware oficial solo lee `config.txt` tras un arranque en frío.

### Botones y PMIC (#20, #1)
- PWR: una pulsación larga apaga el equipo, pero en Arduino hizo falta configurar el AXP2101 para que
  funcionara.
- Inicialización Arduino del AXP2101 que funcionó a un usuario (#1):
  - VBUS 4,36 V / 1500 mA, apagado a 2,9 V.
  - Pulsación de apagado 4 s; TS desactivado; CHGLED apagado.
  - Carga hasta 4,1 V.
  - DC1, ALDO3 y ALDO4 a 3,3 V.

### Otros
- Audio en Arduino: el amplificador (PA) se habilita con **GPIO7**. Ejemplo:
  `05_ArduinoExample/01_Audio_Test` (#18).
- Petición de descargar una imagen por URL a horas fijas con deep sleep: es lo mismo que hace este
  proyecto. Waveshare lo tiene pendiente (#17). El código del issue usa SNTP y un margen de 15 min
  para no repetir la actualización tras el ajuste de hora.
- Para sacar la microSD hay que **levantar la pestaña metálica** del zócalo; no se empuja (#5).
- Las pinzas metálicas que sujetan la pantalla al marco se rompen si se abren a menudo. Varios usuarios
  piden un botón accesible desde fuera (#5, #6).
- Errores de compilación del ejemplo ESP-IDF (xiaozhi):
  - `-Werror=maybe-uninitialized` en freetype con IDF 5.3/5.5 (#16).
  - Versiones de `image_player` / `esp_emote_gfx` en `idf_component.yml` (#3).
  - Faltaba el directorio `components` (#2, #4).
  - Ya están corregidos en el repo.
