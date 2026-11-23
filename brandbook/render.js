// Renderiza brandbook.html a PDF (y vistas previas PNG si se pasa una carpeta)
// Uso: node render.js [carpeta-previews]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1123, height: 794 } });
  await p.goto('file://' + path.join(__dirname, 'brandbook.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.join(__dirname, 'Anthox-PTY-Manual-de-Marca.pdf'), width: '297mm', height: '210mm', printBackground: true, preferCSSPageSize: true });
  if (process.argv[2]) {
    await p.emulateMedia({ media: 'print' });
    const pages = await p.$$('.page');
    for (let i = 0; i < pages.length; i++) {
      await pages[i].screenshot({ path: path.join(process.argv[2], 'p' + String(i + 1).padStart(2, '0') + '.png') });
    }
  }
  await b.close();
})();
