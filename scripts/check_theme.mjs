// Theme behavior without a browser dependency; storage failure is intentional.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
const source = readFileSync(new URL('../tombo.js', import.meta.url), 'utf8');
for (const fail of [null, 'getItem', 'setItem', 'removeItem']) {
  let saved = 'tombo';
  const buttons = ['system', 'tombo', 'hotaru'].map(theme => ({
    getAttribute: () => theme,
    setAttribute(name, value) { this[name] = value; },
  }));
  const root = { dataset: {} };
  const storage = {
    getItem() { if (fail === 'getItem') throw Error('blocked'); return saved; },
    setItem(key, value) { if (fail === 'setItem') throw Error('quota'); saved = value; },
    removeItem() { if (fail === 'removeItem') throw Error('blocked'); saved = null; },
  };
  const context = { window: {}, localStorage: storage, document: {
    documentElement: root, readyState: 'complete',
    body: { appendChild() {} }, createElement: () => ({ setAttribute() {} }),
    addEventListener() {},
    querySelectorAll: selector => selector === '[data-tombo-theme]' ? buttons : [],
  }};
  vm.runInNewContext(source, context);
  const api = context.window.Tombo;
  assert.equal(api.getTheme(), fail === 'getItem' ? 'system' : 'tombo');
  for (const theme of ['hotaru', 'tombo', 'system']) {
    api.setTheme(theme);
    assert.equal(api.getTheme(), theme);
    assert.equal(root.dataset.theme, theme === 'system' ? undefined : theme);
    assert.deepEqual(buttons.map(b => b['aria-pressed']), buttons.map(b => String(b.getAttribute() === theme)));
    if (!fail) assert.equal(saved, theme === 'system' ? null : theme);
  }
  for (const invalid of ['toString', '__proto__', '', null, {}]) {
    api.setTheme(invalid);
    assert.equal(api.getTheme(), 'system');
    assert.equal(root.dataset.theme, undefined);
  }
}
console.log('Theme state and storage failures: PASS');
