// Rellena (y opcionalmente envía) un formulario web de candidatura con Playwright.
// Uso: node practicas/aplicar.mjs <plan.json> [--submit]
// plan.json: { "url": "...", "fields": [{ "selector": "...", "value": "..." }],
//              "files": [{ "selector": "input[type=file]", "path": "practicas/cv/CV_Ziad_Addami_ES.pdf" }],
//              "checks": ["#acepto-privacidad"], "submit": "button[type=submit]" }
// Sin --submit solo rellena y guarda una captura para revisar.
import { createRequire } from 'node:module';
import { readFileSync, mkdirSync } from 'node:fs';
import { execSync } from 'node:child_process';

const require = createRequire(import.meta.url);
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');

const [planPath, flag] = process.argv.slice(2);
const plan = JSON.parse(readFileSync(planPath, 'utf8'));
const shotDir = 'practicas/capturas';
mkdirSync(shotDir, { recursive: true });
const name = planPath.split('/').pop().replace('.json', '');

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const page = await browser.newPage({ locale: 'es-ES' });
await page.goto(plan.url, { waitUntil: 'networkidle' });

for (const f of plan.fields ?? []) await page.fill(f.selector, f.value);
for (const f of plan.files ?? []) await page.setInputFiles(f.selector, f.path);
for (const c of plan.checks ?? []) await page.check(c);
await page.screenshot({ path: `${shotDir}/${name}-relleno.png`, fullPage: true });

if (flag === '--submit') {
  await page.click(plan.submit);
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: `${shotDir}/${name}-enviado.png`, fullPage: true });
  console.log('ENVIADO', page.url());
} else {
  console.log('RELLENADO (no enviado)');
}
await browser.close();
