# ziadaddami.es — portfolio

Mismo principio que la web de R11 (`web/`): un zoom infinito por la subdivisión del rectángulo áureo, con una imagen a pantalla completa por paso y la construcción (cuadrados, espiral, ojo φ) justificando cada encuadre. El motor es el de `web/index.html`; aquí solo cambian los contenidos (`ITEMS`), las imágenes y que la página no se redibuja cuando está quieta.

| Paso | Contenido | Qué justifica la construcción |
|---|---|---|
| 0 | ziad addami | — |
| 1 | Slatted Chair (render) | la silla se inscribe en el cuadrado 1 |
| 2 | Módulo M = 48 (planta y alzado desde el modelo paramétrico) | planta 12M × 12M en el cuadrado 1; alzado 12M × 20M (3:5 ≈ 1:φ) en el rectángulo restante |
| 3 | Lámina A3 | el A3 es 1:√2, no φ: el recorte áureo deja fuera el 13 % |
| 4 | R11 | la web de R11 es esta misma construcción |
| 5 | Sobre mí | — |
| 6 | Contacto | — |

- Imágenes: `python3 ziadaddami/tools/make_images.py` (desde la raíz). Dibuja las vistas con `cad/cadira_breuer.py`, recorta el render y la lámina con `web/tools/golden_crop.py` y captura la web de R11. Los recortes verticales dejan lo importante en el 75 % central, que es lo que se ve en un móvil.
- Archivo único: `python3 web/tools/build_single.py ziadaddami ziadaddami` → `ziadaddami/dist/ziadaddami.html`.
- Por revisar: el correo `hola@ziadaddami.es` y el texto de «Sobre mí» (estudios, ubicación).
