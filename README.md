# home-dashboard

**English** · [Español](#español)

Family dashboard on a 6-colour e-paper frame (**Waveshare ESP32-S3-PhotoPainter**, 7.3",
800×480). The frame wakes up a few times a day, downloads over WiFi an image already prepared by a
home server, draws it and goes back to deep sleep, so it runs for weeks on battery.

![Styles](docs/img/estilos.png)

All data in the image is sample data.

## Why this project exists
I wanted the dashboard in a spot at home **with no power outlets**. I didn't want a cable running
across the wall either, or having to remember every few days to charge the frame or swap a USB
battery. It had to just work: hang it and forget about it for months.

For that the screen has to be **e-paper** (electronic ink), and the hardware has to be designed to
sleep.

### Why e-paper uses so little power
- **It only draws power when the image changes.** An LCD or OLED screen spends energy on every
  frame, 60 times per second, even if the image doesn't change. An e-paper display moves pigment
  particles and they stay where they are. The image is kept **with no power**: even with the
  battery disconnected, the frame keeps showing the last dashboard.
- **No backlight.** You see it with the room's light, like paper. This saves the most
  power-hungry part of a normal screen, and it doesn't glare at night.
- **A family dashboard doesn't need real time.** The date, the weather, the calendar or the school
  lunch menu change a few times a day. Updating the image three times a day is enough (for
  example at 6:00, 16:00 and 22:00).

### How this project takes advantage of it
1. The frame spends almost all its time in **deep sleep**. The ESP32-S3 turns off the CPU, WiFi and
   the display, and only the timer that will wake it up stays on.
2. On waking it connects to WiFi and downloads a **finished** image (dithered, packed and ready for
   the panel). The heavy lifting (fetching data, layout, converting to 6 colours) is done by a
   computer at home that was already on, not by the frame's battery.
3. It draws the image (~25 s refresh) and goes back to sleep. The server tells it how many seconds
   to sleep until the next update (`X-Sleep-Seconds`).
4. If the data hasn't changed, the server replies `204`. The frame doesn't even refresh the panel,
   which is the most expensive part of each cycle.
5. Before sleeping, the unneeded rails (audio, SD, LEDs) are switched off through the AXP2101/TG28
   PMIC.

Each cycle lasts about 30–40 seconds. The rest of the day, more than 99.9 % of the time, the frame
is asleep.

### ~3 months per charge: where the number comes from
It's an estimate, not a measurement. It assumes a 3000 mAh LiPo, three updates a day and the
deep-sleep current given by the Waveshare wiki (≤ 1 mA):

| Item | Rough calculation | mAh/day |
|---|---|---|
| Updates | 3 cycles × ~0.7 mAh (~5 s WiFi + download at ~110 mA, ~25 s panel refresh at ~50 mA) | ~2 |
| Deep sleep | 1 mA × 24 h | 24 |
| **Total** | | **~26** |

Leaving a 15 % margin (the battery never fully drains, it ages and cold reduces its capacity),
that's **~2550 usable mAh ÷ 26 ≈ 100 days, about 3 months**.

The key point of the table is that almost all the consumption is **sleep**, not updates. So
battery life depends mostly on the board's deep-sleep current:
- On Rev 1, users measured ~2 mA (see `docs/issues-photopainter.md`). That gives about 7 weeks.
- Rev 2 fixes some of those PMIC issues, and other firmwares for this board claim to get down to
  tens of µA. At 0.5 mA it would be ~6 months, and at 0.3 mA ~9 months. Every tenth of a mA saved
  in sleep shows up as weeks of battery life.

For comparison: a 10" LCD photo frame draws around 5–10 W when on. With the same battery
(3000 mAh × 3.7 V ≈ 11 Wh) it would last **one or two hours**.

When it's time to charge, just take it down and plug it in via USB-C. The battery icon in the top
right corner gives plenty of warning (red below 20 %).

## Contents
| Folder | What's inside |
|---|---|
| `firmware/` | PlatformIO + Arduino (`espressif32@6.9.0`, XPowersLib). Boot → PMU → WiFi → `GET SERVER_URL` → draw → deep sleep. |
| `server/` | Python + Pillow: `render.py` (layout and 4 styles), `icons.py` (icons drawn with primitives), `epaper.py` (Floyd-Steinberg dither to the 6-colour palette and 4 bpp packing). |
| `docs/` | Hardware and pins, bill of materials, compatible batteries, panel design, known board issues, other displays and links (in Spanish). |

The HTTP server and the data sources (weather, calendar, menu, activities) of the original project
are not included: everyone plugs in their own and passes `render.render()` a `dict` like the one
from `render.fixture()`.

## Try the renderer
```sh
cd server
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python render.py --fixture --estilo comic preview.png   # clasico, comic, pizarra, arcoiris
```
Fonts are the macOS ones (`/System/Library/Fonts`); on another system change the paths in
`render.py`.

## Firmware
```sh
cd firmware
cp include/secrets.example.h include/secrets.h   # WiFi and server URL; not committed to git
pio run -t upload && pio device monitor
```

## Firmware ↔ server contract
`GET SERVER_URL?bat=&usb=&boot=&rssi=&key=` must respond:
- `200` with exactly **192,000 bytes** (4 bpp, 2 px/byte, indices Black=0 White=1 Yellow=2
  Red=3 Blue=5 Green=6): the frame draws it. Produced by `epaper.to_frame(render.render(data))`.
- `204`: nothing new, the frame leaves the panel untouched.
- Both with `X-Sleep-Seconds` (seconds until the next wake-up, clamped to 5 min–24 h).
- Anything else: the frame keeps the image and retries in 30 min.

Details in [docs/hardware.md](docs/hardware.md).

## License
MIT © nachoad. You can reuse the code as long as you keep the copyright notice and the license.

## Inspiration
The idea comes from Wes Bos's [photo-frame-dashboard](https://github.com/wesbos/photo-frame-dashboard):
take a cheap Android photo frame, root it, remove the manufacturer's app and show a full-screen web
page with the family dashboard. It's a great idea, but those frames are tablets with an LCD screen
that is on all day, and they have to be plugged in all the time.

---

# Español

[English](#home-dashboard) · **Español**

Dashboard familiar en un marco e-paper de 6 colores (**Waveshare ESP32-S3-PhotoPainter**, 7,3",
800×480). El marco despierta unas pocas veces al día, descarga por WiFi una imagen ya preparada por
un servidor de casa, la pinta y vuelve a deep sleep, así que funciona semanas con batería.

![Estilos](docs/img/estilos.png)

Todos los datos de la imagen son de ejemplo.

## Por qué existe este proyecto
Yo quería el dashboard en un sitio de casa **donde no hay enchufes**. Tampoco quería un cable
cruzando la pared, ni tener que acordarme cada pocos días de cargar el marco o cambiarle una
batería USB. Tenía que funcionar solo: colgarlo y olvidarse de él durante meses.

Para eso la pantalla tiene que ser **e-paper** (tinta electrónica), y el hardware tiene que estar
pensado para dormir.

### Por qué e-paper gasta tan poco
- **Solo consume al cambiar la imagen.** Una pantalla LCD o OLED gasta energía en cada fotograma,
  60 veces por segundo, aunque la imagen no cambie. Una e-paper mueve unas partículas de pigmento
  y estas se quedan donde están. La imagen se mantiene **sin corriente**: incluso con la batería
  desconectada, el marco sigue mostrando el último dashboard.
- **No tiene retroiluminación.** Se ve con la luz de la habitación, como el papel. Esto ahorra el
  componente que más gasta en una pantalla normal, y además no deslumbra de noche.
- **Un dashboard familiar no necesita tiempo real.** La fecha, el tiempo, el calendario o el menú
  del comedor cambian unas pocas veces al día. Basta con actualizar la imagen tres veces al día
  (por ejemplo a las 6, a las 16 y a las 22 h).

### Cómo se aprovecha en este proyecto
1. El marco pasa casi todo el tiempo en **deep sleep**. El ESP32-S3 apaga la CPU, el WiFi y la
   pantalla, y solo queda encendido el temporizador que lo despertará.
2. Al despertar se conecta al WiFi y descarga una imagen **ya terminada** (dithered, empaquetada y
   lista para el panel). El trabajo pesado (descargar datos, maquetar, convertir a 6 colores) lo
   hace un ordenador de casa que ya estaba encendido, no la batería del marco.
3. Pinta la imagen (~25 s de refresco) y vuelve a dormir. El servidor le dice cuántos segundos
   tiene que dormir hasta la próxima actualización (`X-Sleep-Seconds`).
4. Si los datos no han cambiado, el servidor responde `204`. El marco ni siquiera refresca el
   panel, que es la parte más cara de cada ciclo.
5. Antes de dormir se apagan los raíles que no hacen falta (audio, SD, LEDs) a través del PMIC
   AXP2101/TG28.

Cada ciclo dura unos 30–40 segundos. El resto del día, más del 99,9 % del tiempo, el marco está
dormido.

### ~3 meses con una carga: de dónde sale la cifra
Es una estimación, no una medida. Supone una LiPo de 3000 mAh, tres actualizaciones al día y la
corriente en deep sleep que da la wiki de Waveshare (≤ 1 mA):

| Concepto | Cálculo aproximado | mAh/día |
|---|---|---|
| Actualizaciones | 3 ciclos × ~0,7 mAh (~5 s de WiFi + descarga a ~110 mA, ~25 s de refresco del panel a ~50 mA) | ~2 |
| Deep sleep | 1 mA × 24 h | 24 |
| **Total** | | **~26** |

Si se deja un margen del 15 % (la batería no se vacía del todo, envejece y el frío le quita
capacidad), quedan **~2550 mAh útiles ÷ 26 ≈ 100 días, unos 3 meses**.

Lo importante de la tabla es que casi todo el consumo es el **sueño**, no las actualizaciones.
Por eso la autonomía depende sobre todo de la corriente en deep sleep de la placa:
- En la Rev 1, usuarios midieron ~2 mA (ver `docs/issues-photopainter.md`). Con eso salen unas
  7 semanas.
- La Rev 2 corrige parte de esos problemas del PMIC, y otros firmwares para esta placa dicen bajar
  a decenas de µA. Con 0,5 mA serían ~6 meses, y con 0,3 mA ~9 meses. Cada décima de mA ahorrada
  en sueño se nota en semanas de autonomía.

Por comparar: un marco de fotos LCD de 10" consume del orden de 5–10 W encendido. Con esa misma
batería (3000 mAh × 3,7 V ≈ 11 Wh) duraría **una o dos horas**.

Cuando toca cargarlo, basta con descolgarlo y enchufarlo por USB-C. El icono de batería de la
esquina superior derecha avisa con tiempo (rojo por debajo del 20 %).

## Contenido
| Carpeta | Qué hay |
|---|---|
| `firmware/` | PlatformIO + Arduino (`espressif32@6.9.0`, XPowersLib). Arranque → PMU → WiFi → `GET SERVER_URL` → pinta → deep sleep. |
| `server/` | Python + Pillow: `render.py` (layout y 4 estilos), `icons.py` (iconos dibujados con primitivas), `epaper.py` (dither Floyd-Steinberg a la paleta de 6 colores y empaquetado a 4 bpp). |
| `docs/` | Hardware y pines, lista de materiales, baterías compatibles, diseño del panel, problemas conocidos de la placa, otras pantallas y enlaces. |

El servidor HTTP y las fuentes de datos (tiempo, calendario, menú, actividades) del proyecto
original no se incluyen: cada uno conecta las suyas y pasa a `render.render()` un `dict` como el de
`render.fixture()`.

## Probar el render
```sh
cd server
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python render.py --fixture --estilo comic preview.png   # clasico, comic, pizarra, arcoiris
```
Las fuentes son las de macOS (`/System/Library/Fonts`); en otro sistema hay que cambiar las rutas
de `render.py`.

## Firmware
```sh
cd firmware
cp include/secrets.example.h include/secrets.h   # WiFi y URL del servidor; no se sube a git
pio run -t upload && pio device monitor
```

## Contrato firmware ↔ servidor
`GET SERVER_URL?bat=&usb=&boot=&rssi=&key=` debe responder:
- `200` con exactamente **192 000 bytes** (4 bpp, 2 px/byte, índices Black=0 White=1 Yellow=2
  Red=3 Blue=5 Green=6): el marco la pinta. Se obtiene con `epaper.to_frame(render.render(data))`.
- `204`: nada nuevo, el marco no toca el panel.
- Ambas con `X-Sleep-Seconds` (segundos hasta el próximo despertar, limitado a 5 min–24 h).
- Cualquier otra cosa: el marco conserva la imagen y reintenta en 30 min.

Detalle en [docs/hardware.md](docs/hardware.md).

## Licencia
MIT © nachoad. Puedes reutilizar el código manteniendo el aviso de copyright y la licencia.

## Inspiración
La idea viene de [photo-frame-dashboard](https://github.com/wesbos/photo-frame-dashboard), de Wes
Bos: coger un marco de fotos Android barato, rootearlo, quitar la app del fabricante y poner una
web a pantalla completa con el dashboard de la familia. Es una idea estupenda, pero esos marcos
son tablets con pantalla LCD encendida todo el día y tienen que estar enchufados siempre.
