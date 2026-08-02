(() => {
  'use strict';

  const button = document.querySelector('[data-back-to-top]');
  if (!button) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let frameRequested = false;

  function updateVisibility() {
    const scrollPosition = Math.max(window.scrollY, document.documentElement.scrollTop);
    button.hidden = scrollPosition < Math.min(640, window.innerHeight);
    frameRequested = false;
  }

  window.addEventListener('scroll', () => {
    if (frameRequested) return;
    frameRequested = true;
    window.requestAnimationFrame(updateVisibility);
  }, { passive: true });

  window.addEventListener('pageshow', updateVisibility);
  window.visualViewport?.addEventListener('resize', updateVisibility);

  button.addEventListener('click', () => {
    const heading = document.querySelector('h1');
    window.scrollTo({ top: 0, behavior: reducedMotion.matches ? 'auto' : 'smooth' });
    if (heading) {
      heading.tabIndex = -1;
      heading.focus({ preventScroll: true });
      heading.addEventListener('blur', () => heading.removeAttribute('tabindex'), { once: true });
    }
  });

  updateVisibility();
})();
