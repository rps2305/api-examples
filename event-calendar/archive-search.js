(() => {
  const search = document.querySelector('[data-archive-search]');
  const list = document.querySelector('.archive-grid, .lowlands-list');
  if (!search || !list) return;
  const input = search.querySelector('input');
  const clear = search.querySelector('[data-search-clear]');
  const status = search.querySelector('[role="status"]');
  const items = [...list.children];
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('nl').trim();
  const searchable = items.map(item => normalize(item.textContent));
  const update = () => {
    const terms = normalize(input.value).split(/\s+/).filter(Boolean);
    let count = 0;
    items.forEach((item, index) => {
      const match = terms.every(term => searchable[index].includes(term));
      item.hidden = !match;
      if (match) count++;
    });
    status.textContent = terms.length ? `${count} ${count === 1 ? 'resultaat' : 'resultaten'} gevonden.` : '';
    clear.disabled = !input.value;
  };
  input.addEventListener('input', update);
  clear.addEventListener('click', () => { input.value = ''; update(); input.focus(); });
  search.hidden = false;
  update();
})();
