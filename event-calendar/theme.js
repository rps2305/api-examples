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
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setupToggle, { once: true });
  else setupToggle();
})();
