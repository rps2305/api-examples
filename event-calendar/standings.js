(function () {
  const panel = document.querySelector('#standings-panel');
  const containers = [document.querySelector('#standings-a'), document.querySelector('#standings-b')];
  const statusLine = document.querySelector('#standings-status');
  if (!panel || containers.some(container => !container)) return;

  const stat = (entry, name) => {
    const item = entry.stats?.find(candidate => candidate.name === name);
    return item?.displayValue ?? '';
  };

  async function renderStandings() {
    try {
      const response = await fetch('/api/standings', { cache: 'no-cache' });
      if (!response.ok) throw new Error('standings unavailable');
      const data = await response.json();
      const standings = data.children?.[0]?.standings;
      const entries = Array.isArray(standings?.entries) ? standings.entries : [];
      if (!entries.length) throw new Error('no standings entries');

      const seasonLabel = document.querySelector('#standings-season');
      if (seasonLabel) {
        const rawSeason = standings.seasonDisplayName || standings.season?.displayName || '';
        const yearMatch = rawSeason.match(/^\d{4}-\d{2}/);
        seasonLabel.textContent = yearMatch ? yearMatch[0].replace('-', '/') : rawSeason;
      }
      const fullTableLink = document.querySelector('#standings-link');
      if (fullTableLink) {
        const tableHref = standings.links?.find?.(link => link.rel?.includes('standings'))?.href;
        if (tableHref) fullTableLink.href = tableHref;
      }

      const buildRow = entry => {
        const isTwente = entry.team?.displayName === 'FC Twente' || String(entry.team?.id) === '152';
        const tr = document.createElement('tr');
        if (isTwente) {
          tr.classList.add('standings-current');
          tr.setAttribute('aria-current', 'true');
        }
        const position = document.createElement('th');
        position.scope = 'row';
        position.textContent = stat(entry, 'rank');
        tr.append(position);
        for (const value of [entry.team?.displayName ?? '', stat(entry, 'gamesPlayed'), stat(entry, 'wins'), stat(entry, 'ties'), stat(entry, 'losses'), stat(entry, 'points'), stat(entry, 'pointsFor'), stat(entry, 'pointsAgainst')]) {
          const cell = document.createElement('td');
          cell.textContent = value;
          tr.append(cell);
        }
        return tr;
      };

      const halfway = Math.ceil(entries.length / 2);
      containers[0].replaceChildren(...entries.slice(0, halfway).map(buildRow));
      containers[1].replaceChildren(...entries.slice(halfway).map(buildRow));
      panel.hidden = false;
      if (statusLine) statusLine.hidden = true;
    } catch {
      if (statusLine) {
        statusLine.dataset.state = 'error';
        statusLine.textContent = 'De stand kon niet worden geladen. Bekijk de volledige stand via de link hierboven.';
      }
    }
  }

  if ('requestIdleCallback' in window) window.requestIdleCallback(renderStandings, { timeout: 3_000 });
  else window.setTimeout(renderStandings, 0);
}());