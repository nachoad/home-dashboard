# Baterías para el PhotoPainter

Solo hace falta si se compra el PhotoPainter **sin batería** (SKU 32753 o Amazon B0FWRHXCC3 "No Bat").
La opción más segura es el kit con la batería de 1500 mAh de Waveshare.

**Buena relación €/mAh:** songyea 1S 1C de 3000 mAh, pack de 2 por 16,99 €
(https://www.amazon.es/dp/B0FP5G3HHS). Mide 65×35×10 mm y pesa 48,5 g. Tiene placa de protección
(sobrecorriente 1,8–2,1 A, 1C) y conector Micro JST 1.25. Al recibirla: medir el hueco y
comprobar la polaridad (abajo).

## Conector y polaridad (esquemático de Waveshare)
- Conector **J2 "PH1.25-2P"**: paso 1.25 mm, de la familia Molex PicoBlade 51021. En las tiendas
  aparece como "MX1.25", "PH1.25" o "Micro JST 1.25".
- **Pin 1 = BAT+** (va a BAT, pin 33 del AXP2101). **Pin 2 = GND.**
- Hay otro PH1.25-2P (**J3**) para la pila del RTC (VBACKUP): la LiPo **no** va ahí.
- Y un tercero (**H1**) para el altavoz (salida de audio, AGND): tampoco.
- **No sirven:** PH2.0 / JST-PH 2.0 mm / "PHR-02" (paso más ancho) ni SH1.0.

## Antes de enchufar
1. Busca en la placa, junto a J2, la marca de "+" o de "1".
2. Pon el conector de la batería al lado, sin enchufarlo: el cable **rojo** tiene que caer en el
   lado del "+". Si no hay serigrafía, mide la batería con el multímetro (+3,7–4,2 V en el rojo).
3. Si viene al revés, no la conectes. Puedes invertir los pines levantando la pestaña de cada
   terminal con una aguja, o devolverla.
4. Mide el hueco que queda detrás del panel: las celdas de 2000–3000 mAh tienen ~10 mm de grosor.

## Candidatas en Amazon.es (consultado 2026-10-12)
Ningún anuncio dice qué pin es el "+", así que hay que hacer siempre la comprobación de arriba.
Amazon oculta el precio en la ficha ("añádelo a la cesta"). Los precios son los "a partir de"
del selector de variantes o del carrusel de productos similares. Las medidas y el resto de datos
salen de la ficha y no están verificados.

Autonomía orientativa a ~26 mAh/día y 85 % de capacidad útil (1 mA en sleep, 3 actualizaciones/día, ver `bom.md`).

| Batería | Capacidad | Medidas (mm) | Conector | Protección | Uds. | Precio | Autonomía | Notas | Link |
|---|---|---|---|---|---|---|---|---|---|
| Hosifiy 802525 | 400 mAh | 25×25×8,6 | PH 1,25 mm, cable 5 cm | Sí | 1 | desde 15,99 € | ~2 semanas | Avisa de comprobar la polaridad. Poca capacidad. | https://www.amazon.es/dp/B0G5NNPK7Z |
| Seamuing | 1000 mAh | 45×25×9 | Micro JST 1.25 | Sí | 1 | agotada | ~4–5 semanas | 4,2★ (72) | https://www.amazon.es/dp/B09B77CC7L |
| RmtcBal 803040 | 1000 mAh | 41×30×8 | **Dudoso:** el título dice "PHR" y las viñetas dicen 1,25 mm | Sí (PCM) | 1 | sin precio | ~4–5 semanas | Cables rojo/negro. Comprobar el conector en las fotos. | https://www.amazon.es/dp/B0G64BKS1V |
| RmtcBal 803040 (otro anuncio) | 1000 mAh | 40×30×8 | "JST 1,25 mm" (no dice PH ni PHR) | No lo dice | 1 | sin precio | ~4–5 semanas | 3,4★ (6). Cables rojo/negro, sin indicar el +. Consultado 2026-10-15. | https://www.amazon.es/dp/B0GLFDG5JK |
| Sunkoo 803040 1S | 1000 mAh | ~40×30×8 (por el modelo; no leí la ficha) | "Micro JST de 1,25 mm, 2 pines" | Sí (PCM) | 1 | desde 13,87 € | ~4–5 semanas | 4,5★ (2). Anunciada para ESP32. Mejor de las de 1000 mAh. Consultado 2026-10-15. | https://www.amazon.es/dp/B0GJSH4J3S |
| Sunkoo 103450 1S (variante del anuncio anterior) | 2000 mAh | ~50×34×**10**, 35 g | "Micro JST 1,25 mm"; ficha: "Molex 1.25" | Sí (PCM: corte 4,2 V / 2,75 V) | 1 | 14,11 € | ~9 semanas | 5,0★ (3). Carga máx. 0,5C = 1000 mA (el AXP2101 carga a 500 mA: OK). **Recomendada si cabe.** El mismo anuncio tiene la 103665 de 3000 mAh (65×36×10) a 16,95 €. Consultado 2026-10-15. | https://www.amazon.es/dp/B0GJSH4J3S |
| Seamuing 1S 1C | 1100 mAh | 50×30×8 o 45×25×10 (la ficha se contradice) | Micro JST 1.25 | Sí | 4 | agotada | ~5 semanas | 4,4★ (276) | https://www.amazon.es/dp/B087LTZW61 |
| **songyea 1S 1C** | 3000 mAh | 65×35×10, 48,5 g | Micro JST 1.25 | Sí (sobrecorriente 1,8–2,1 A) | 2 | 16,99 € | ~14 semanas | 4,6★ (42). La mejor relación €/mAh; con 65 mm de largo, comprobar que cabe. | https://www.amazon.es/dp/B0FP5G3HHS |
| songyea 1S 1C | 3000 mAh | 65×35×10 | Micro JST 1.25 | Sí | 4 | desde 23,99 € | ~14 semanas | 4,9★ (24) | https://www.amazon.es/dp/B0F99KLK2Y |

### Finas (5–8 mm de grosor) con conector de 1.25 mm
Para cuando el hueco detrás del panel es pequeño. Vendedor HXJN (marca HXJNLDC), envío por Amazon.
El precio no aparece en la ficha. Datos de la ficha, sin verificar.

| Batería | Capacidad | Medidas (mm) | Conector | Protección | Polaridad | Autonomía | Link |
|---|---|---|---|---|---|---|---|
| HXJNLDC 603040 | 800 mAh | 40,5×30×**6** | "JST Pitch 1.25mm" | Sí (IC Seiko) | "cable rojo es positivo" | ~3–4 semanas | https://www.amazon.es/dp/B09YQ2C1KR |
| HXJNLDC 602530 | 450 mAh | 31×25×**6** | "JST Pitch 1.25mm" | Sí (IC Seiko) | "cable rojo es positivo" | ~2 semanas | https://www.amazon.es/dp/B0D4V9NWKD |
| RmtcBal 803040 | 1000 mAh | 41×30×**8** | Dudoso ("PHR" en el título, 1,25 mm en las viñetas) | Sí (PCM) | Rojo/negro | ~4 semanas | https://www.amazon.es/dp/B0G64BKS1V |
| Sunkoo 803040 1S | 1000 mAh | ~40×30×**8** | "Micro JST de 1,25 mm" | Sí (PCM) | No lo dice | ~4–5 semanas | https://www.amazon.es/dp/B0GJSH4J3S |

- **Ojo con la misma marca:** la HXJNLDC 603048 de 1000 mAh (B09YQ1Y3CY) también mide 6 mm, pero lleva
  conector de **2.0 mm**. No vale.
- En AliExpress hay 503450 (5 mm, ~1000 mAh), 603450 (6 mm, ~1200 mAh) y 504050 (5 mm, ~1500 mAh)
  anunciadas con "JST 1.25mm 2pin" o "MX1.25". Los mismos modelos también salen con PH2.0, así que hay
  que elegir bien la variante. Ej.: https://www.aliexpress.us/item/3256808521080209.html
- Las BricoGeek finas (503048 de 5 mm, 603450 de 6 mm) son PH2.0: solo sirven cambiando el conector.

**1500 mAh:** en Amazon.es solo encontré modelos con conector PH2.0 (por ejemplo EEMB 524261,
HRYHWASE 803450), que **no encajan**. Con 1.25 mm, la única opción de 1500 mAh es la batería de
Waveshare que viene con el kit.

## Fuera de Amazon (consultado 2026-10-12)
En tiendas españolas y de la UE **no he encontrado ninguna LiPo con conector de 1.25 mm confirmado**.

| Tienda | Batería | Precio | Resultado |
|---|---|---|---|
| BricoGeek (ES) | 750–2200 mAh: 503048, 603050, 603450, 103450, 903759… | 5,60–7,90 € + IVA | La ficha dice "conector tipo Molex/JST" sin indicar el paso, pero enlaza la hoja de datos de **JST PH (2.0 mm)**. **No valen** sin cambiar el conector. Son buenas candidatas para hacerlo: 750 mAh 48×30×5 mm, 1200 mAh 52×35×6 mm. https://tienda.bricogeek.com/126-baterias-lipo |
| Welectron (DE) | PKCell 500–2500 mAh | 4,50–7,70 € | "PH Stecker" / "JST PH2.0". **No valen.** |
| Botland (PL), Kubii (FR), BerryBase (DE) | — | — | Ninguna LiPo de 1.25 mm en el catálogo. |
| The Pi Hut (UK) | PKCell 1200 mAh, PicoBlade 1.25 mm (Molex 51021), 62×35×5 mm | 8 £ | **Vale**, pero **solo envía la batería a Inglaterra y Gales**. https://thepihut.com/products/1200mah-3-7v-lipo-battery-1-25mm-picoblade-connector |
| AliExpress (CN) | 1000–2000 mAh "MX1.25 2P" / "JST 1.25mm 2pin" | ~3–5 $/ud. o packs de 10 | **Valen** si el anuncio dice 1.25 mm. Envío de 2–4 semanas. Las capacidades no siempre cuadran con el modelo, y hay que comprobar la polaridad. P. ej. 902040 1000 mAh: https://www.aliexpress.com/item/1005006995943957.html · 2000 mAh 704060: https://www.aliexpress.us/item/3256809668623187.html · pack 10 uds. 600–2300 mAh: https://www.aliexpress.us/item/3256808521080209.html |

Conclusión: para comprar en España sin esperar, lo mejor es Amazon (tabla de arriba). Otra opción es una
BricoGeek fina (750 o 1200 mAh, 5–6 mm) cambiándole el conector por un cable MX1.25.
