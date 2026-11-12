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
  const dateFormat = new Intl.DateTimeFormat('nl-NL', { timeZone: 'Europe/Amsterdam', weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
  function showMatches(listId, statusId, matches, emptyText) {
    const list = document.getElementById(listId), status = document.getElementById(statusId);
    if (!list || !status) return;
    if (!matches.length) { status.textContent = emptyText; return; }
    list.replaceChildren(...matches.map(match => {
      const li = document.createElement('li');
      const date = document.createElement('time'); date.dateTime = match.date; date.textContent = dateFormat.format(new Date(match.date));
      const name = document.createElement('strong'); name.textContent = match.name;
      li.append(date, name);
      if (match.score) { const score = document.createElement('span'); score.className = 'football-score'; score.textContent = match.score; li.append(score); }
      return li;
    }));
    status.hidden = true;
  }
  fetch('events.json', { cache: 'no-cache' }).then(response => { if (!response.ok) throw Error(); return response.json(); }).then(events => {
    const matches = events.filter(e => e.source === 'fc-twente' && new Date(e.startDate) >= new Date()).sort((a,b) => new Date(a.startDate) - new Date(b.startDate)).slice(0, 8).map(e => ({ date: e.startDate, name: e.name }));
    showMatches('fixtures-list', 'fixtures-status', matches, 'Er zijn momenteel geen komende wedstrijden beschikbaar.');
  }).catch(() => { document.getElementById('fixtures-status').textContent = 'Wedstrijden konden niet worden geladen. Bekijk het programma bij FC Twente.'; });
  fetch('/api/fc-twente-results').then(response => { if (!response.ok) throw Error(); return response.json(); }).then(data => {
    const matches = (data.events || []).flatMap(event => {
      const competition = event.competitions?.[0], teams = competition?.competitors || [];
      if (!competition?.status?.type?.completed) return [];
      const home = teams.find(team => team.homeAway === 'home'), away = teams.find(team => team.homeAway === 'away');
      if (!home || !away || home.score?.displayValue == null || away.score?.displayValue == null) return [];
      return [{ date: event.date, name: `${home.team.displayName} – ${away.team.displayName}`, score: `${home.score.displayValue} – ${away.score.displayValue}` }];
    }).sort((a,b) => new Date(b.date) - new Date(a.date)).slice(0, 8);
    showMatches('results-list', 'results-status', matches, 'Er zijn momenteel geen uitslagen beschikbaar.');
  }).catch(() => { document.getElementById('results-status').textContent = 'Uitslagen konden niet worden geladen. Bekijk de uitslagen bij ESPN.'; });
}());