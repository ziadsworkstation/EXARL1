# R11 — web del estudio

Sin dependencias ni build: abrir en el navegador o servir la carpeta tal cual.

## `index.html` — versión φ (actual)

Página ultra minimalista sobre un rectángulo áureo dibujado en `<canvas>`. El scroll (rueda, gesto táctil o flechas) hace un zoom continuo hacia el ojo de la espiral: cada paso entra en el siguiente cuadrado (escala ×φ, giro 90°). Como la figura es autosemejante, el recorrido es un bucle infinito en ambos sentidos. Cada cuadrado lleva un contenido (`ITEMS` en el script) y su lado `φ⁻ⁿ`; el HUD muestra la profundidad `n` y la escala `1 : φⁿ`. Al soltar, la vista se asienta en el cuadrado más cercano.

Las imágenes de `web/img/` están recortadas a 1:1 para llenar exactamente su cuadrado áureo; se asignan con la clave `img` de cada elemento de `ITEMS` (r11, fundadores y contacto quedan en blanco). Son imágenes de referencia: antes de publicar, sustituirlas por fotografía propia o con derechos.

Para cambiar textos, edita el array `ITEMS`. El contenido también está en HTML oculto (`<main class="sr">`) para lectores de pantalla y buscadores.

## `editorial.html` — versión editorial (anterior)

- Tipografías (Google Fonts): Inter Tight (texto y marca), Instrument Serif (cursivas editoriales), JetBrains Mono (pies y metadatos).
- Paleta: hormigón `#E4E2DE`, tinta `#121212`, metacrilato rojo `#E8251B`, vidrio cobalto `#1C2FD8`.
- Las imágenes de proyecto están hechas con CSS. Para usar fotos reales, sustituye el `<div class="art …">` de cada `.frame` por un `<img>` con `object-fit:cover`.
- Secciones: Estudio · Enfoque (producto + espacio + experiencia) · Proyectos · Servicios · Para empresas (departamento de diseño externo) · Proceso · Materiales · Equipo · Contacto.
- Contenido provisional por revisar: proyectos P-01–P-04 (inventados), correo `hola@r11.studio`, ciudad, redes sociales, retratos de los fundadores (ahora iniciales).
