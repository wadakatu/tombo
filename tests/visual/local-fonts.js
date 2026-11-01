import { readFileSync } from 'node:fs';

// Preserve the site's family names and Martian Mono's width axis, but serve
// locked font files locally so Google Fonts availability cannot change a run.
const fonts = [
  ['instrument-sans', 'index.css'],
  ['m-plus-2', 'index.css'],
  ['martian-mono', 'standard.css'],
].map(([name, file]) => {
  const path = `node_modules/@fontsource-variable/${name}`;
  return readFileSync(`${path}/${file}`, 'utf8')
    .replaceAll(" Variable'", "'")
    .replaceAll('url(./files/', `url(http://127.0.0.1:4173/${path}/files/`);
}).join('\n');

export async function useLocalFonts(page) {
  await page.route('**/*', route => {
    const url = new URL(route.request().url());
    if (url.hostname === 'fonts.googleapis.com') {
      return route.fulfill({ contentType: 'text/css', body: fonts });
    }
    if (url.origin === 'http://127.0.0.1:4173') return route.continue();
    return route.abort();
  });
}
