const agenda = document.querySelector('#agenda');
const status = document.querySelector('#status');
const search = document.querySelector('#search');
const networkStatus = document.querySelector('#network-status');
const agendaSummary = document.querySelector('#agenda-summary');
const initialView = new URLSearchParams(location.search).get('view');
let filter = 'all';
let query = '';
let todayOnly = initialView === 'today';
let recommendedOnly = initialView === 'recommended';
let hasPrerenderedAgenda = agenda.dataset.prerendered === 'true';
const dateFormat = new Intl.DateTimeFormat('nl-NL', { weekday: 'long', day: 'numeric', month: 'long' });
const timeFormat = new Intl.DateTimeFormat('nl-NL', {
  hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Amsterdam',
});
const suggestionForm = document.querySelector('#suggestion-form');
const suggestionStatus = document.querySelector('#suggestion-status');
const themeToggle = document.querySelector('#theme-toggle');
const sourcePriority = new Map([
  ['metropool', 0],
  ['de-cactus', 1],
  ['fc-twente', 2],
  ['oogst', 3],
]);
const allowedSources = new Set(['metropool', 'de-cactus', 'fc-twente', 'oogst', 'hengelo', 'feestdagen']);
let suggestionToken = '';

document.documentElement.classList.remove('no-js');

function syncThemeToggle() {
  if (!themeToggle) return;
  const dark = document.documentElement.dataset.theme === 'dark';
  themeToggle.setAttribute('aria-label', dark ? 'Gebruik lichte modus' : 'Gebruik donkere modus');
  themeToggle.setAttribute('aria-pressed', String(dark));
  themeToggle.querySelector('[data-theme-label]').textContent = dark ? 'Licht' : 'Donker';
}

syncThemeToggle();
themeToggle?.addEventListener('click', () => {
  const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = theme;
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#090d14' : '#111827');
  try { localStorage.setItem('uit-vandaag-theme', theme); } catch { /* Preference remains active for this visit. */ }
  syncThemeToggle();
});

function plainText(value, maximumLength = 300) {
  return String(value ?? '')
    .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, '')
    .slice(0, maximumLength)
    .trim();
}

function safeUrl(value) {
  try {
    const url = new URL(value);
    return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
  } catch {
    return '';
  }
}

function normalizeEvent(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return null;
  const source = plainText(value.source, 30);
  const name = plainText(value.name, 300);
  const startDate = plainText(value.startDate, 40);
  if (!allowedSources.has(source) || !name || !/^\d{4}-\d{2}-\d{2}(?:T.+)?$/.test(startDate) || Number.isNaN(Date.parse(startDate))) return null;
  return {
    '@type': source === 'fc-twente' ? 'SportsEvent' : 'Event',
    name,
    startDate,
    location: plainText(value.location, 300),
    genre: plainText(value.genre, 200),
    url: safeUrl(value.url),
    ticketUrl: safeUrl(value.ticketUrl),
    source,
    isHome: value.isHome === true,
    soldOut: value.soldOut === true,
    recommended: value.recommended === true,
    tasteReason: plainText(value.tasteReason, 300),
  };
}

function element(tagName, className, text) {
  const node = document.createElement(tagName);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function externalLink(url, label, className = '') {
  if (!url) return null;
  const link = element('a', className, label);
  link.href = url;
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  return link;
}

function showStatusError(message) {
  status.dataset.state = 'error';
  const reload = element('a', '', 'Vernieuw de pagina');
  reload.href = '';
  const download = element('a', '', 'download de agenda');
  download.href = 'events.ics';
  status.replaceChildren(document.createTextNode(`${message} `), reload, document.createTextNode(' of '), download, document.createTextNode('.'));
}

function icalText(event) {
  const escapeIcal = value => String(value || '').replace(/\\/g, '\\\\').replace(/[,;]/g, '\\$&').replace(/\n/g, '\\n');
  const dateValue = event.startDate.length === 10
    ? `;VALUE=DATE:${event.startDate.replaceAll('-', '')}`
    : `:${new Date(event.startDate).toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '')}`;
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
  if (event.source === 'feestdagen') return '🇳🇱 Feestdag';
  if (event.source === 'fc-twente') return '⚽ FC Twente';
  if (event.source === 'de-cactus') return '🌵 DE CACTUS';
  if (event.source === 'oogst') return '🌾 Oogst';
  if (event.source === 'hengelo') return '🏛️ Hengelo';
  return `🎵 Metropool ${event.location || ''}`.trim();
}

function eventElement(event) {
  const time = event.source === 'feestdagen' ? 'Hele dag' : event.startDate.length === 10 ? 'Tijd volgt' : timeFormat.format(new Date(event.startDate));
  const kind = event.source === 'feestdagen' ? '🇳🇱 Nationale feestdag' : event.source === 'fc-twente' ? '⚽ Voetbal' : event.genre ? `🎵 ${event.genre}` : '🎤 Live';
  const article = element('article', `event ${event.source}${event.isHome ? ' fc-home' : ''}`);
  article.append(element('p', 'event-time', time), element('p', 'venue', venueLabel(event)));

  if (event.recommended || event.soldOut) {
    const badges = element('p', 'event-badges');
    if (event.recommended) {
      const tasteBadge = element('span', 'taste-badge', '★ Voor jou');
      tasteBadge.title = event.tasteReason || 'Past bij Ronalds muzieksmaak';
      badges.append(tasteBadge);
    }
    if (event.soldOut) badges.append(element('span', 'sold-out-badge', 'Uitverkocht'));
    article.append(badges);
  }

  article.append(element('h3', '', event.name));
  article.append(element('p', 'meta', `${kind}${event.location ? ` · 📍 ${event.location}` : ''}`));
  const links = element('p', 'event-links');
  const infoLabel = event.source === 'fc-twente' ? 'Wedstrijd ↗' : event.source === 'feestdagen' ? 'Rijksoverheid ↗' : 'Info ↗';
  const infoLink = externalLink(event.url, infoLabel);
  const ticketLink = event.ticketUrl !== event.url ? externalLink(event.ticketUrl, 'Tickets ↗', 'tickets') : null;
  if (infoLink) links.append(infoLink);
  if (ticketLink) links.append(ticketLink);
  const calendarButton = element('button', 'event-calendar-button', '🗓');
  calendarButton.type = 'button';
  calendarButton.dataset.eventCalendar = JSON.stringify(event);
  calendarButton.setAttribute('aria-label', `Voeg ${event.name} toe aan agenda`);
  calendarButton.title = 'Voeg toe aan agenda';
  links.append(calendarButton);
  article.append(links);
  return article;
}

function twenteDateKey(date = new Date()) {
  const parts = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Europe/Amsterdam', year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(date);
  const values = Object.fromEntries(parts.map(part => [part.type, part.value]));
  return `${values.year}-${values.month}-${values.day}`;
}

function eventDateKey(event) {
  return event.startDate.length === 10 ? event.startDate : twenteDateKey(new Date(event.startDate));
}

function dateKeyAfter(dateKey, days) {
  const date = new Date(`${dateKey}T12:00:00Z`);
  date.setUTCDate(date.getUTCDate() + days);
  return date.toISOString().slice(0, 10);
}

function updateAgendaSummary(events) {
  if (!agendaSummary) return;
  const today = twenteDateKey();
  const weekEnd = dateKeyAfter(today, 7);
  const todayCount = events.filter(event => eventDateKey(event) === today).length;
  const weekCount = events.filter(event => {
    const date = eventDateKey(event);
    return date >= today && date < weekEnd;
  }).length;
  const todayLabel = todayCount === 1 ? 'evenement' : 'evenementen';
  agendaSummary.textContent = `Vandaag ${todayCount} ${todayLabel}, deze week ${weekCount}.`;
}

function agendaOrder(first, second) {
  const priority = (sourcePriority.get(first.source) ?? 10) - (sourcePriority.get(second.source) ?? 10);
  return priority || first.startDate.localeCompare(second.startDate) || first.name.localeCompare(second.name, 'nl');
}

function render(events) {
  const today = twenteDateKey();
  const shown = events.filter(event =>
    (filter === 'all' || event.source === filter)
    && (!recommendedOnly || event.recommended === true)
    && (!todayOnly || eventDateKey(event) === today)
    && JSON.stringify(event).toLowerCase().includes(query));
  const groups = Object.groupBy(shown, eventDateKey);
  status.dataset.state = 'ready';
  status.textContent = `${shown.length} ${shown.length === 1 ? 'plan' : 'plannen'}${todayOnly ? ' vandaag' : ' in de agenda'}${recommendedOnly ? ' voor jou' : ''}`;
  const emptyMessage = recommendedOnly ? 'Geen sterke muziekmatches in deze selectie. Bekijk de volledige agenda.' : todayOnly ? 'Vandaag staat er niets in deze selectie. Bekijk de volledige agenda.' : 'Geen plannen gevonden. Probeer een andere zoekterm.';
  if (hasPrerenderedAgenda && filter === 'all' && !todayOnly && !recommendedOnly && !query) return;
  hasPrerenderedAgenda = false;
  agenda.dataset.prerendered = 'false';
  const content = document.createDocumentFragment();
  for (const [date, items] of Object.entries(groups)) {
    const day = element('section', 'day');
    const heading = element('div', 'day-heading');
    const title = element('h2');
    const dateNode = element('time', '', dateFormat.format(new Date(`${date}T12:00:00`)));
    dateNode.dateTime = date;
    title.append(dateNode);
    heading.append(title, element('span', '', `${items.length} ${items.length === 1 ? 'plan' : 'plannen'}`));
    const dayEvents = element('div', 'day-events');
    dayEvents.append(...items.sort(agendaOrder).map(eventElement));
    day.append(heading, dayEvents);
    content.append(day);
  }
  if (!shown.length) content.append(element('p', 'empty', emptyMessage));
  agenda.replaceChildren(content);
}

function syncNetworkStatus() {
  if (!networkStatus) return;
  networkStatus.hidden = navigator.onLine;
  networkStatus.textContent = navigator.onLine
    ? ''
    : 'Je bent offline. De laatst opgeslagen agenda blijft beschikbaar; versturen en externe links werken weer zodra je verbinding hebt.';
}

syncNetworkStatus();
window.addEventListener('online', syncNetworkStatus);
window.addEventListener('offline', syncNetworkStatus);

try {
  const parsedEvents = JSON.parse(document.querySelector('#event-data').textContent);
  if (!Array.isArray(parsedEvents)) throw new TypeError('Event feed must be an array');
  const events = parsedEvents.map(normalizeEvent).filter(Boolean);
  updateAgendaSummary(events);
  if (todayOnly) {
    const todayButton = document.querySelector('[data-today-filter]');
    todayButton.classList.add('active');
    todayButton.setAttribute('aria-pressed', 'true');
  }
  if (recommendedOnly) {
    const recommendedButton = document.querySelector('[data-recommended-filter]');
    recommendedButton.classList.add('active');
    recommendedButton.setAttribute('aria-pressed', 'true');
  }
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
  document.querySelector('[data-today-filter]').addEventListener('click', event => {
    todayOnly = !todayOnly;
    event.currentTarget.classList.toggle('active', todayOnly);
    event.currentTarget.setAttribute('aria-pressed', String(todayOnly));
    render(events);
  });
  document.querySelector('[data-recommended-filter]').addEventListener('click', event => {
    recommendedOnly = !recommendedOnly;
    event.currentTarget.classList.toggle('active', recommendedOnly);
    event.currentTarget.setAttribute('aria-pressed', String(recommendedOnly));
    render(events);
  });
  search.addEventListener('input', event => { query = event.target.value.toLowerCase(); render(events); });
} catch {
  showStatusError('De agenda kon niet worden geladen.');
}

async function refreshSuggestionToken() {
  const response = await fetch('/api/suggestions/token', { cache: 'no-store', credentials: 'same-origin' });
  if (!response.ok) throw new Error('token unavailable');
  suggestionToken = (await response.json()).token;
}

if (suggestionForm) {
  refreshSuggestionToken().catch(() => {
    suggestionStatus.textContent = 'De ideeënbus is tijdelijk niet beschikbaar.';
  });
  suggestionForm.addEventListener('submit', async event => {
    event.preventDefault();
    const submitButton = suggestionForm.querySelector('button[type="submit"]');
    const fields = new FormData(suggestionForm);
    submitButton.disabled = true;
    suggestionStatus.textContent = 'Suggestie versturen…';
    try {
      if (!suggestionToken) await refreshSuggestionToken();
      const response = await fetch('/api/suggestions', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token: suggestionToken,
          name: fields.get('name'),
          email: fields.get('email'),
          category: fields.get('category'),
          message: fields.get('message'),
          website: fields.get('website'),
        }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || 'Versturen mislukt.');
      suggestionForm.reset();
      suggestionStatus.textContent = 'Bedankt! Je suggestie is naar Ronald verstuurd.';
      suggestionToken = '';
      await refreshSuggestionToken();
    } catch (error) {
      suggestionStatus.textContent = error.message || 'Versturen mislukt. Probeer het later opnieuw.';
      suggestionToken = '';
      refreshSuggestionToken().catch(() => {});
    } finally {
      submitButton.disabled = false;
    }
  });
}

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js', { scope: '/' }).catch(() => {
      // The agenda remains fully usable online when service workers are unavailable.
    });
  });
}
