(function () {
  const links = [...document.querySelectorAll('[data-lightbox]')];
  if (!links.length || typeof HTMLDialogElement === 'undefined') return;

  const gallery = [];
  const seen = new Map();
  // The album defines the order; photos used only inline are appended.
  const ordered = [...links.filter(link => link.closest('.photo-grid')), ...links.filter(link => !link.closest('.photo-grid'))];
  for (const link of ordered) {
    const key = link.dataset.lightbox;
    if (!seen.has(key)) {
      const image = link.querySelector('img');
      const caption = link.closest('figure')?.querySelector('figcaption')?.textContent
        || link.querySelector('span')?.textContent || image?.alt || '';
      seen.set(key, gallery.length);
      gallery.push({ href: link.href, srcset: image?.getAttribute('srcset') || '', alt: image?.alt || '', caption, width: image?.width, height: image?.height });
    }
  }

  const dialog = document.createElement('dialog');
  dialog.className = 'lightbox';
  dialog.setAttribute('aria-label', 'Fotoweergave');
  dialog.innerHTML = '<figure class="lightbox-figure"><img class="lightbox-image" alt="" /><figcaption class="lightbox-caption"></figcaption></figure>'
    + '<button type="button" class="lightbox-close" aria-label="Sluiten">×</button>'
    + '<button type="button" class="lightbox-nav lightbox-prev" aria-label="Vorige foto">‹</button>'
    + '<button type="button" class="lightbox-nav lightbox-next" aria-label="Volgende foto">›</button>'
    + '<p class="lightbox-count" aria-live="polite"></p>';
  document.body.append(dialog);
  const image = dialog.querySelector('.lightbox-image');
  const caption = dialog.querySelector('.lightbox-caption');
  const count = dialog.querySelector('.lightbox-count');
  let index = 0;
  let opener = null;

  function show(next) {
    index = (next + gallery.length) % gallery.length;
    const item = gallery[index];
    image.srcset = item.srcset;
    image.sizes = '96vw';
    image.src = item.href;
    image.alt = item.alt;
    for (const offset of [1, -1]) new Image().src = gallery[(index + offset + gallery.length) % gallery.length].href;
    caption.textContent = item.caption;
    count.textContent = `${index + 1} van ${gallery.length}`;
  }

  document.addEventListener('click', event => {
    const link = event.target.closest('[data-lightbox]');
    if (link) {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.button) return;
      event.preventDefault();
      opener = link;
      show(seen.get(link.dataset.lightbox));
      dialog.showModal();
      return;
    }
    if (event.target === dialog) dialog.close();
    if (event.target.closest('.lightbox-close')) dialog.close();
    if (event.target.closest('.lightbox-prev')) show(index - 1);
    if (event.target.closest('.lightbox-next')) show(index + 1);
  });
  // Swipe left/right on touch screens to move through the album.
  let touchStart = null;
  dialog.addEventListener('touchstart', event => {
    touchStart = event.touches.length === 1 ? { x: event.touches[0].clientX, y: event.touches[0].clientY } : null;
  }, { passive: true });
  dialog.addEventListener('touchend', event => {
    if (!touchStart) return;
    const touch = event.changedTouches[0];
    const dx = touch.clientX - touchStart.x;
    const dy = touch.clientY - touchStart.y;
    touchStart = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(index + (dx < 0 ? 1 : -1));
  });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') show(index - 1);
    if (event.key === 'ArrowRight') show(index + 1);
  });
  dialog.addEventListener('close', () => { image.removeAttribute('src'); image.removeAttribute('srcset'); opener?.focus(); });
}());
