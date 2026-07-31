const agenda = document.querySelector('#agenda');
const status = document.querySelector('#status');
const search = document.querySelector('#search');
let filter = 'all';
let query = '';
const dateFormat = new Intl.DateTimeFormat('nl-NL', { weekday: 'long', day: 'numeric', month: 'long' });
const timeFormat = new Intl.DateTimeFormat('nl-NL', { hour: '2-digit', minute: '2-digit' });

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' })[char]);
}

function safeUrl(value) {
  try {
    const url = new URL(value);
    return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
  } catch {
    return '';
  }
}

function icalText(event) {
  const escapeIcal = value => String(value || '').replace(/\\/g, '\\\\').replace(/[,;]/g, '\\$&').replace(/\n/g, '\\n');
  const start = event.startDate.replace(/[-:]/g, '').replace(/\.\d+/, '').replace('+02:00', '').replace('+01:00', '');
  const dateValue = event.startDate.length === 10 ? `;VALUE=DATE:${start}` : `:${start}`;
  const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Uit Vandaag Twente//NL', 'BEGIN:VEVENT', `UID:${encodeURIComponent(`${event.name}-${event.startDate}`)}@event-calendar.puntuale.nl`, `DTSTART${dateValue}`, `SUMMARY:${escapeIcal(event.name)}`];
  if (event.location) lines.push(`LOCATION:${escapeIcal(event.location)}`);
  if (event.url) lines.push(`URL:${event.url}`);
  return `${lines.concat('END:VEVENT', 'END:VCALENDAR').join('\r\n')}\r\n`;
}

function downloadEvent(event) {
  const blob = new Blob([icalText(event)], { type: 'text/calendar;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const anchor = Object.assign(document.createElement('a'), { href: url, download: 'uit-vandaag.ics' });
  anchor.click();
  URL.revokeObjectURL(url);
}

function venueLabel(event) {
  if (event.source === 'fc-twente') return '⚽ FC Twente';
  if (event.source === 'de-cactus') return '🌵 DE CACTUS';
  if (event.source === 'oogst') return '🌾 Oogst';
  if (event.source === 'hengelo') return '🏛️ Hengelo';
  return `🎵 Metropool ${event.location || ''}`.trim();
}

function eventMarkup(event) {
  const time = event.startDate.length === 10 ? 'Tijd volgt' : timeFormat.format(new Date(event.startDate));
  const kind = event.source === 'fc-twente' ? '⚽ Voetbal' : event.genre ? `🎵 ${escapeHtml(event.genre)}` : '🎤 Live';
  const infoUrl = safeUrl(event.url);
  const ticketUrl = safeUrl(event.ticketUrl);
  const links = [
    infoUrl && `<a href="${escapeHtml(infoUrl)}" target="_blank" rel="noreferrer">${event.source === 'fc-twente' ? 'Wedstrijd' : 'Info'} ↗</a>`,
    ticketUrl && ticketUrl !== infoUrl && `<a class="tickets" href="${escapeHtml(ticketUrl)}" target="_blank" rel="noreferrer">Tickets ↗</a>`,
  ].filter(Boolean).join('');
  return `<article class="event ${event.source}${event.isHome ? ' fc-home' : ''}">
    <p class="event-time">${escapeHtml(time)}</p><p class="venue">${escapeHtml(venueLabel(event))}</p>
    <h2>${escapeHtml(event.name)}</h2><p class="meta">${kind}${event.location ? ` · 📍 ${escapeHtml(event.location)}` : ''}</p>
    <p class="event-links">${links}<button class="event-calendar-button" type="button" data-event-calendar="${escapeHtml(JSON.stringify(event))}" aria-label="${escapeHtml(`Voeg ${event.name} toe aan agenda`)}" title="Voeg toe aan agenda">🗓</button></p></article>`;
}

function render(events) {
  const shown = events.filter(event => (filter === 'all' || event.source === filter) && JSON.stringify(event).toLowerCase().includes(query));
  const groups = Object.groupBy(shown, event => event.startDate.slice(0, 10));
  status.textContent = `${shown.length} plannen in de agenda`;
  agenda.innerHTML = Object.entries(groups).map(([date, items]) => `<section class="day"><div class="day-heading"><time datetime="${date}">${dateFormat.format(new Date(`${date}T12:00:00`))}</time><span>${items.length} ${items.length === 1 ? 'plan' : 'plannen'}</span></div><div class="day-events">${items.map(eventMarkup).join('')}</div></section>`).join('') || '<p class="empty">Geen plannen gevonden. Probeer een andere zoekterm.</p>';
}

try {
  const events = JSON.parse(document.querySelector('#event-data').textContent);
  render(events);
  agenda.addEventListener('click', event => {
    const button = event.target.closest('[data-event-calendar]');
    if (button) downloadEvent(JSON.parse(button.dataset.eventCalendar));
  });
  document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
    document.querySelector('[data-filter].active').classList.remove('active');
    document.querySelector('[data-filter][aria-pressed="true"]').setAttribute('aria-pressed', 'false');
    button.classList.add('active'); filter = button.dataset.filter; render(events);
    button.setAttribute('aria-pressed', 'true');
  }));
  search.addEventListener('input', event => { query = event.target.value.toLowerCase(); render(events); });
} catch { status.textContent = 'De agenda kon niet worden geladen. Bouw de agenda opnieuw op.'; }
