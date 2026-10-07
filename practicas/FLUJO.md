# Flujo diario de búsqueda y candidatura de prácticas

Instrucciones que sigue la rutina diaria. Lee primero `practicas/perfil.md`.

## 1. Buscar
- Con WebSearch, busca ofertas publicadas en los últimos ~7 días. Consultas (ES, CA y EN):
  - «prácticas diseño industrial Barcelona», «becario diseño de producto Barcelona»,
    «pràctiques disseny industrial Barcelona», «industrial design intern Barcelona»,
    «prácticas ingeniería de producto CAD Barcelona», «becario I+D desarrollo de producto Barcelona»,
    «TFG en empresa diseño industrial Barcelona».
- Fuentes típicas: LinkedIn, InfoJobs, Indeed, Welcome to the Jungle, Jobfluent, iAgora, PrimerEmpleo,
  webs de estudios de diseño y de empresas industriales, borsa de pràctiques UPC.
- Ignora las URL ya presentes en `practicas/seen.json`.

## 2. Filtrar y puntuar (0-10)
- Sigue las preferencias y exclusiones de `perfil.md`.
- +3 diseño de producto/industrial, +2 CAD/prototipado/I+D, +2 Barcelona o alrededores, +1 admite convenio
  curricular, +1 posibilidad de TFG, +1 media jornada / compatible con clases.
- Descarta lo que tenga encaje < 6, ofertas caducadas o que no sean prácticas.

## 3. Preparar la candidatura (encaje ≥ 6)
- Carta de presentación: en el idioma de la oferta, 180-250 palabras, con la plantilla de
  `practicas/cartas/plantilla.md`. Debe nombrar la empresa y algo concreto de la oferta o de sus productos.
  Solo datos de `perfil.md`; nada inventado.
- Formulario: prepara las respuestas de cada pregunta. Preguntas abiertas («¿por qué nosotros?») con 2-4 frases.
- Guarda la carta en `practicas/cartas/AAAA-MM-DD_empresa.md`.

## 4. Enviar
- **Envío automático** solo si se cumplen todas: encaje ≥ 7, formulario web público sin login ni CAPTCHA
  (Greenhouse, Lever, Workable, Teamtailor, Typeform, formulario propio de la empresa), y todos los
  campos obligatorios se pueden responder con `perfil.md`.
  - Escribe `practicas/planes/<empresa>.json` y ejecuta primero `node practicas/aplicar.mjs <plan>`
    (sin enviar), revisa la captura, y luego `--submit`.
  - Estado: «Enviada automáticamente».
- En cualquier otro caso (LinkedIn, InfoJobs, Indeed, portales con login, envío por email, datos que
  faltan, CAPTCHA, el sitio no es accesible desde la red): no se envía. Estado «Pendiente de tu acción»,
  con la carta y las respuestas listas para copiar y pegar, y en Notas qué falta exactamente.
- Nunca respondas «sí» a preguntas de requisitos que no cumpla, no pagues nada, no crees cuentas.

## 5. Registrar
- Una entrada por oferta (también las descartadas con encaje ≥ 5, con motivo) en el formulario Jotform
  «Candidaturas prácticas – Ziad Addami» (ID 262794159654067) con `create_submission`.
- Añade las URL procesadas a `practicas/seen.json`.
- Commit y push a la rama del repo con mensaje «Prácticas: búsqueda AAAA-MM-DD (N enviadas, M pendientes)».
- Termina con un resumen corto: enviadas, pendientes (con enlace) y descartadas.
