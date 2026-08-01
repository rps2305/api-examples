(() => {
  document.documentElement.classList.remove('no-js');
  let preference = '';
  try {
    preference = localStorage.getItem('uit-vandaag-theme') || '';
  } catch {
    // Storage can be unavailable in strict privacy modes; system preference still works.
  }
  const theme = ['light', 'dark'].includes(preference)
    ? preference
    : (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.dataset.theme = theme;
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#090d14' : '#111827');
})();
