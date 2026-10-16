# home-dashboard

Dashboard familiar en un marco e-paper de 6 colores (**Waveshare ESP32-S3-PhotoPainter**, 7,3",
800×480). El marco despierta unas pocas veces al día, descarga por WiFi una imagen ya preparada por
un servidor de casa, la pinta y vuelve a deep sleep, así que funciona semanas con batería.

![Estilos](docs/img/estilos.png)

Todos los datos de la imagen son de ejemplo.

## Por qué existe este proyecto
La idea viene de [photo-frame-dashboard](https://github.com/wesbos/photo-frame-dashboard), de Wes
Bos: coger un marco de fotos Android barato, rootearlo, quitar la app del fabricante y poner una
web a pantalla completa con el dashboard de la familia. Es una idea estupenda, pero esos marcos
son tablets con pantalla LCD encendida todo el día y tienen que estar enchufados siempre.

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

### ~7 meses con una carga: de dónde sale la cifra
Es una estimación, no una medida. Supone una placa Rev 2, una LiPo de 3000 mAh y tres
actualizaciones al día:

| Concepto | Cálculo aproximado | mAh/día |
|---|---|---|
| Actualizaciones | 3 ciclos × ~35 s × ~50–60 mA de media (WiFi + refresco del panel) | ~1,5 |
| Deep sleep | ~0,4 mA × 24 h | ~9,6 |
| **Total** | | **~11** |

3000 mAh ÷ 11 mAh/día ≈ 270 días. Si se deja un margen del 20 % (la batería no se vacía del todo,
envejece y el frío le quita capacidad), quedan **~2400 mAh útiles ÷ 11 ≈ 7 meses**.

Lo importante de la tabla es que casi todo el consumo es el **sueño**, no las actualizaciones.
Por eso la autonomía depende sobre todo de la corriente en deep sleep de la placa:
- La wiki de Waveshare habla de ≤ 1 mA. Con 1 mA salen unos 3 meses.
- En la Rev 1, usuarios midieron ~2 mA (ver `docs/issues-photopainter.md`). Con eso salen unas
  6 semanas.
- La Rev 2 corrige parte de esos problemas del PMIC, y otros firmwares para esta placa dicen bajar
  a decenas de µA. Cada décima de mA ahorrada en sueño se nota en semanas de autonomía.

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
