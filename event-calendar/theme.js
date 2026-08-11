(() => {
  const THEME_KEY = 'uit-vandaag-theme';

  function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#090d14' : '#111827');
  }

  function syncToggle() {
    const toggle = document.querySelector('#theme-toggle');
    if (!toggle) return;
    const dark = document.documentElement.dataset.theme === 'dark';
    toggle.setAttribute('aria-label', dark ? 'Gebruik lichte modus' : 'Gebruik donkere modus');
    toggle.setAttribute('aria-pressed', String(dark));
    const label = toggle.querySelector('[data-theme-label]');
    if (label) label.textContent = dark ? 'Licht' : 'Donker';
  }

  function setupToggle() {
    syncToggle();
    document.querySelector('#theme-toggle')?.addEventListener('click', () => {
      const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      applyTheme(theme);
      try { localStorage.setItem(THEME_KEY, theme); } catch { /* Preference remains active for this visit. */ }
      syncToggle();
    });
  }

  function setupMenu() {
    const menu = document.querySelector('.site-menu');
    const toggle = document.querySelector('[data-menu-toggle]');
    const panel = document.querySelector('#site-menu-panel');
    if (!menu || !toggle || !panel) return;
    const close = () => { panel.hidden = true; toggle.setAttribute('aria-expanded', 'false'); };
    toggle.addEventListener('click', () => {
      const open = panel.hidden;
      panel.hidden = !open;
      toggle.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('click', event => { if (!menu.contains(event.target)) close(); });
    document.addEventListener('keydown', event => { if (event.key === 'Escape') close(); });
  }

  function markCurrentPage() {
    const currentPath = location.pathname.replace(/\/$/, '/index.html');
    document.querySelectorAll('a[href]').forEach(link => {
      const target = new URL(link.href, location.href);
      if (target.origin === location.origin && target.pathname === currentPath) link.setAttribute('aria-current', 'page');
    });
  }

  document.documentElement.classList.remove('no-js');
  let preference = '';
  try {
    preference = localStorage.getItem(THEME_KEY) || '';
  } catch {
    // Storage can be unavailable in strict privacy modes; system preference still works.
  }
  const theme = ['light', 'dark'].includes(preference)
    ? preference
    : (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  applyTheme(theme);
  const setup = () => { setupToggle(); setupMenu(); markCurrentPage(); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup, { once: true });
  else setup();
})();
