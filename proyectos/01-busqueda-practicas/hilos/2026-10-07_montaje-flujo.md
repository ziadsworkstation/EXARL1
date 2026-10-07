# Hilo 2026-10-07 · Montaje del flujo automático de prácticas

Sesión: https://claude.ai/code/session_01NBCaXiPo6ueRQFN3ioz9nH

## Lo que pidió Ziad
Un flujo automático que cada día busque ofertas de prácticas, aplique, redacte las cartas de
presentación y rellene los formularios. Subió sus dos CV (ES y EN).

## Decisiones
- Ubicación: Barcelona y alrededores.
- Tipo: diseño de producto / industrial, ingeniería / I+D / CAD, TFG en empresa.
- Modalidad: curriculares, desde ya.
- Envío: automático (solo donde sea técnicamente posible: formulario web público sin login ni CAPTCHA).
- Tracker en Jotform (a petición de Ziad), con `practicas/registro.md` como copia en el repo.
- Software añadido al perfil: SolidWorks, NX, AutoCAD, Photoshop, Illustrator (nivel básico).
- IA: usa Claude y ChatGPT a diario con conectores externos para automatizar tareas.

## Lo que se hizo
- `practicas/` con perfil, flujo, plantilla de carta, script de relleno de formularios (probado en local),
  registro y CVs.
- Formulario Jotform «Candidaturas prácticas – Ziad Addami».
- Rutina diaria «Prácticas diarias – Ziad» (trig_01V2WS3rLeDgMsJxKU836shh), aviso por push y email.
- Carta de ejemplo: `practicas/cartas/EJEMPLO_becario-disenador-industrial.md`.

## Bloqueos detectados
- La red del entorno bloquea webs de empleo y ziadaddami.es → no hay envío automático todavía.
- La rutina se creó sin el conector Jotform ni el repo enlazado; hay que añadirlos desde claude.ai.
- No hay Gmail conectado → las candidaturas por email quedan preparadas para enviarlas a mano.
- LinkedIn, InfoJobs y el convenio UPC requieren login → siempre serán acción de Ziad.
