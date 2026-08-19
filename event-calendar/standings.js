(function () {
  const panel = document.querySelector('#standings-panel');
  const container = document.querySelector('#standings');
  if (!panel || !container) return;

  const stat = (entry, name) => {
    const item = entry.stats?.find(candidate => candidate.name === name);
    return item?.displayValue ?? '';
  };

  const statItem = (label, value) => {
    const item = document.createElement('div');
    const term = document.createElement('dt');
    const detail = document.createElement('dd');
    term.textContent = label;
    detail.textContent = value;
    item.append(term, detail);
    return item;
  };

  async function renderStandings() {
    try {
      const response = await fetch('/api/standings', { cache: 'no-cache' });
      if (!response.ok) throw new Error('standings unavailable');
      const data = await response.json();
      const standings = data.children?.[0]?.standings;
      const entries = Array.isArray(standings?.entries) ? standings.entries : [];
      const twente = entries.find(entry =>
        entry.team?.displayName === 'FC Twente' || String(entry.team?.id) === '152');
      if (!twente) throw new Error('FC Twente missing from standings');

      const seasonLabel = document.querySelector('#standings-season');
      if (seasonLabel) seasonLabel.textContent = standings.seasonDisplayName || standings.season?.displayName || '';
      const fullTableLink = document.querySelector('#standings-link');
      if (fullTableLink) {
        const tableHref = standings.links?.find?.(link => link.rel?.includes('standings'))?.href;
        if (tableHref) fullTableLink.href = tableHref;
      }

      container.replaceChildren(
        statItem('Positie', `${stat(twente, 'rank')}e`),
        statItem('Gespeeld', stat(twente, 'gamesPlayed')),
        statItem('Winst', stat(twente, 'wins')),
        statItem('Gelijk', stat(twente, 'ties')),
        statItem('Verlies', stat(twente, 'losses')),
        statItem('Punten', stat(twente, 'points')),
      );
      panel.hidden = false;
    } catch {
      panel.hidden = true;
    }
  }

  if ('requestIdleCallback' in window) window.requestIdleCallback(renderStandings, { timeout: 3_000 });
  else window.setTimeout(renderStandings, 0);
}());