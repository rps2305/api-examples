window.setTimeout(() => {
  const status = document.querySelector('#status[data-state="loading"]');
  if (!status) return;
  status.dataset.state = 'error';
  const reload = document.createElement('a');
  reload.href = '';
  reload.textContent = 'Vernieuw de pagina';
  const download = document.createElement('a');
  download.href = 'events.ics';
  download.textContent = 'download de agenda';
  status.replaceChildren(
    document.createTextNode('De agenda kon niet worden gestart. '),
    reload,
    document.createTextNode(' of '),
    download,
    document.createTextNode('.'),
  );
}, 8000);
