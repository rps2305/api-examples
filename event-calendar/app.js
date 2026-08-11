const agenda = document.querySelector('#agenda');
const status = document.querySelector('#status');
const search = document.querySelector('#search');
const monthFilter = document.querySelector('#month-filter');
const yearFilter = document.querySelector('#year-filter');
const dateFilter = document.querySelector('#date-filter');
const cityFilter = document.querySelector('#city-filter');
const typeFilter = document.querySelector('#type-filter');
const networkStatus = document.querySelector('#network-status');
const agendaSummary = document.querySelector('#agenda-summary');
const loadMoreButton = document.querySelector('[data-load-more]');
const initialParams = new URLSearchParams(location.search);
const initialView = initialParams.get('view');
const PAGE_SIZE = 60;
let filter = 'all';
let selectedSources = new Set();
let query = '';
let selectedDate = '';
let selectedCity = '';
let selectedType = '';
let selectedMonth = '';
let selectedYear = '';
let todayOnly = initialParams.get('today') === '1' || initialView === 'today';
let recommendedOnly = initialParams.get('recommended') === '1' || initialView === 'recommended';
let visibleLimit = PAGE_SIZE;
let hasPrerenderedAgenda = agenda.dataset.prerendered === 'true';
const DEFAULT_EVENT_DURATION_MINUTES = 120;
const dateFormat = new Intl.DateTimeFormat('nl-NL', { weekday: 'long', day: 'numeric', month: 'long' });
const timeFormat = new Intl.DateTimeFormat('nl-NL', {
  hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Amsterdam',
});
const suggestionForm = document.querySelector('#suggestion-form');
const suggestionStatus = document.querySelector('#suggestion-status');
const sourcePriority = new Map([
  ['metropool', 0],
  ['de-cactus', 1],
  ['fc-twente', 2],
  ['oogst', 3],
  ['bijzonder', 4],
]);
const allowedSources = new Set(['metropool', 'de-cactus', 'fc-twente', 'oogst', 'hengelo', 'feestdagen', 'persoonlijk', 'bijzonder']);
let suggestionToken = '';

document.documentElement.classList.remove('no-js');

function plainText(value, maximumLength = 300) {
  return String(value ?? '')
    .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, '')
    .slice(0, maximumLength)
    .trim();
}

function safeUrl(value) {
  if (!value) return '';
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
  const rawEndDate = plainText(value.endDate, 40);
  if (!allowedSources.has(source) || !name || !/^\d{4}-\d{2}-\d{2}(?:T.+)?$/.test(startDate) || Number.isNaN(Date.parse(startDate))) return null;
  const endDate = /^\d{4}-\d{2}-\d{2}(?:T.+)?$/.test(rawEndDate) && !Number.isNaN(Date.parse(rawEndDate)) ? rawEndDate : '';
  return {
    '@type': source === 'fc-twente' ? 'SportsEvent' : 'Event',
    name,
    startDate,
    endDate,
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
  const icalDateValue = value => value.length === 10
    ? `;VALUE=DATE:${value.replaceAll('-', '')}`
    : `:${new Date(value).toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '')}`;
  const normalizedStart = event.startDate.length === 10 ? event.startDate : new Date(event.startDate).toISOString();
  const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Uit Vandaag Twente//NL', 'BEGIN:VEVENT', `UID:${encodeURIComponent(`${event.name}-${event.startDate}`)}@event-calendar.puntuale.nl`, `DTSTART${icalDateValue(normalizedStart)}`, `SUMMARY:${escapeIcal(event.name)}`];
  let endDate = event.endDate;
  if (!endDate && event.startDate.length !== 10) {
    endDate = new Date(new Date(event.startDate).getTime() + DEFAULT_EVENT_DURATION_MINUTES * 60_000).toISOString();
  }
  if (endDate) lines.push(`DTEND${icalDateValue(endDate)}`);
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

function setShareFeedback(button, label, title = label) {
  const originalLabel = button.dataset.originalLabel || button.textContent;
  button.dataset.originalLabel = originalLabel;
  button.textContent = label;
  button.title = title;
  button.disabled = true;
  window.setTimeout(() => {
    button.textContent = originalLabel;
    button.title = 'Deel de informatielink';
    button.disabled = false;
  }, 1_800);
}

async function copyShareLink(url) {
  if (navigator.clipboard?.writeText && window.isSecureContext) {
    await navigator.clipboard.writeText(url);
    return;
  }
  const field = document.createElement('textarea');
  field.value = url;
  field.setAttribute('readonly', '');
  field.style.cssText = 'position:fixed;top:0;left:0;opacity:0;pointer-events:none';
  document.body.append(field);
  field.select();
  field.setSelectionRange(0, field.value.length);
  const copied = document.execCommand('copy');
  field.remove();
  if (!copied) throw new Error('copy unavailable');
}

async function shareEvent(event, button) {
  if (!event.url) return;
  // Safari's Web Share implementation is more reliable with its minimal data set.
  const shareData = { title: event.name, url: event.url };
  try {
    if (navigator.share) {
      await navigator.share(shareData);
      setShareFeedback(button, 'Gedeeld');
      return;
    }
  } catch (error) {
    if (error?.name === 'AbortError') return;
    // Some Safari versions expose Web Share but reject it for this context.
  }
  try {
    await copyShareLink(event.url);
    setShareFeedback(button, 'Link gekopieerd');
  } catch {
    // A system prompt is deliberately the final fallback: it works in iOS
    // browsers that block both Web Share and programmatic clipboard access.
    window.prompt('Kopieer deze link:', event.url);
    setShareFeedback(button, 'Link tonen', 'De link is geopend om te kopiëren');
  }
}

function venueLabel(event) {
  if (event.source === 'feestdagen') return 'Feestdag';
  if (event.source === 'persoonlijk') return 'Persoonlijk';
  if (event.source === 'bijzonder') return 'Bijzonder';
  if (event.source === 'fc-twente') return 'FC Twente';
  if (event.source === 'de-cactus') return 'De Cactus';
  if (event.source === 'oogst') return 'Oogst';
  if (event.source === 'hengelo') return 'Hengelo';
  return `Metropool ${event.location || ''}`.trim();
}

function eventElement(event) {
  const time = event.source === 'feestdagen' ? 'Hele dag' : event.startDate.length === 10 ? 'Tijd volgt' : timeFormat.format(new Date(event.startDate));
  const kind = event.source === 'feestdagen' ? 'Nationale feestdag' : event.source === 'fc-twente' ? 'Voetbal' : event.genre || 'Live';
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
  const ticketLink = event.ticketUrl && (event.ticketUrl !== event.url || event.source === 'de-cactus')
    ? externalLink(event.ticketUrl, 'Tickets ↗', 'tickets')
    : null;
  if (infoLink) links.append(infoLink);
  if (ticketLink) links.append(ticketLink);
  if (ticketLink) links.classList.add('has-ticket');
  if (event.url) {
    const shareButton = element('button', 'event-share-button', 'Delen');
    shareButton.type = 'button';
    shareButton.dataset.eventShare = JSON.stringify(event);
    shareButton.setAttribute('aria-label', `Delen: ${event.name}`);
    shareButton.title = 'Deel de informatielink';
    links.append(shareButton);
  }
  const calendarButton = element('button', 'event-calendar-button', 'Zet in agenda');
  calendarButton.type = 'button';
  calendarButton.dataset.eventCalendar = JSON.stringify(event);
  calendarButton.setAttribute('aria-label', `Zet in agenda: ${event.name}`);
  calendarButton.title = 'Download dit evenement als iCalendar-bestand';
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

function eventMonthKey(event) {
  return eventDateKey(event).slice(0, 7);
}

function populateDateFilters(events) {
  const months = [...new Set(events.map(eventMonthKey))].sort();
  const years = [...new Set(months.map(month => month.slice(0, 4)))];
  const label = new Intl.DateTimeFormat('nl-NL', { month: 'long', year: 'numeric' });
  monthFilter.replaceChildren(element('option', '', 'Alle maanden'));
  monthFilter.firstElementChild.value = '';
  months.forEach(month => {
    const option = element('option', '', label.format(new Date(`${month}-01T12:00:00`)));
    option.value = month;
    monthFilter.append(option);
  });
  yearFilter.replaceChildren(element('option', '', 'Alle jaren'));
  yearFilter.firstElementChild.value = '';
  years.forEach(year => {
    const option = element('option', '', year);
    option.value = year;
    yearFilter.append(option);
  });
}

function applyUrlFilters(events) {
  const params = new URLSearchParams(location.search);
  const availableSources = new Set(events.map(event => event.source));
  selectedSources = new Set((params.get('source') || '').split(',').filter(source => availableSources.has(source)));
  filter = selectedSources.size === 1 ? [...selectedSources][0] : 'all';

  search.value = params.get('q') || '';
  query = search.value.toLowerCase();

  const requestedMonth = params.get('month') || '';
  selectedMonth = [...monthFilter.options].some(option => option.value === requestedMonth) ? requestedMonth : '';
  const requestedYear = params.get('year') || '';
  selectedYear = [...yearFilter.options].some(option => option.value === requestedYear) ? requestedYear : '';
  if (selectedMonth) selectedYear = selectedMonth.slice(0, 4);
  const legacyView = params.get('view');
  todayOnly = params.get('today') === '1' || legacyView === 'today';
  recommendedOnly = params.get('recommended') === '1' || legacyView === 'recommended';
  selectedDate = /^\d{4}-\d{2}-\d{2}$/.test(params.get('date') || '') ? params.get('date') : '';
  selectedCity = (params.get('city') || '').toLowerCase();
  selectedType = (params.get('type') || '').toLowerCase();

  monthFilter.value = selectedMonth;
  yearFilter.value = selectedYear;
  dateFilter.value = selectedDate;
  cityFilter.value = [...cityFilter.options].some(option => option.value === selectedCity) ? selectedCity : '';
  typeFilter.value = selectedType;
  document.querySelectorAll('[data-filter]').forEach(button => {
    const active = button.dataset.filter === 'all' ? selectedSources.size === 0 : selectedSources.has(button.dataset.filter);
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  const todayButton = document.querySelector('[data-today-filter]');
  todayButton.classList.toggle('active', todayOnly);
  todayButton.setAttribute('aria-pressed', String(todayOnly));
  const recommendedButton = document.querySelector('[data-recommended-filter]');
  recommendedButton.classList.toggle('active', recommendedOnly);
  recommendedButton.setAttribute('aria-pressed', String(recommendedOnly));
}

function syncFiltersToUrl({ replace = false } = {}) {
  const url = new URL(location.href);
  ['source', 'q', 'month', 'year', 'date', 'city', 'type', 'today', 'recommended', 'view'].forEach(name => url.searchParams.delete(name));
  if (selectedSources.size) url.searchParams.set('source', [...selectedSources].join(','));
  if (search.value) url.searchParams.set('q', search.value);
  if (selectedMonth) url.searchParams.set('month', selectedMonth);
  if (selectedYear) url.searchParams.set('year', selectedYear);
  if (selectedDate) url.searchParams.set('date', selectedDate);
  if (selectedCity) url.searchParams.set('city', selectedCity);
  if (selectedType) url.searchParams.set('type', selectedType);
  if (todayOnly) url.searchParams.set('today', '1');
  if (recommendedOnly) url.searchParams.set('recommended', '1');
  if (`${url.pathname}${url.search}${url.hash}` === `${location.pathname}${location.search}${location.hash}`) return;
  history[replace ? 'replaceState' : 'pushState']({}, '', url);
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

function syncLoadMore(visibleCount, totalCount) {
  if (!loadMoreButton) return;
  const remaining = Math.max(0, totalCount - visibleCount);
  loadMoreButton.hidden = remaining === 0;
  loadMoreButton.textContent = remaining
    ? `Toon volgende ${Math.min(PAGE_SIZE, remaining)} plannen`
    : 'Alle plannen zijn zichtbaar';
}

function render(events) {
  if (hasPrerenderedAgenda && visibleLimit === PAGE_SIZE && selectedSources.size === 0 && !todayOnly && !recommendedOnly && !query && !selectedMonth && !selectedYear && !selectedDate && !selectedCity && !selectedType) {
    const visibleCount = Math.min(PAGE_SIZE, events.length);
    status.dataset.state = 'ready';
    status.textContent = `${visibleCount} van ${events.length} plannen zichtbaar`;
    syncLoadMore(visibleCount, events.length);
    return;
  }
  const today = twenteDateKey();
  const matching = events.filter(event =>
    (!selectedSources.size || selectedSources.has(event.source))
    && (!recommendedOnly || event.recommended === true)
    && (!todayOnly || eventDateKey(event) === today)
    && (!selectedMonth || eventMonthKey(event) === selectedMonth)
    && (!selectedYear || eventDateKey(event).startsWith(`${selectedYear}-`))
    && (!selectedDate || eventDateKey(event) === selectedDate)
    && (!selectedCity || `${event.location} ${venueLabel(event)}`.toLowerCase().includes(selectedCity))
    && (!selectedType || `${event.genre} ${event.name}`.toLowerCase().includes(selectedType))
    && (!query || `${event.name} ${event.location} ${event.genre} ${event.source}`.toLowerCase().includes(query)));
  const shown = matching.slice(0, visibleLimit);
  const groups = Object.groupBy(shown, eventDateKey);
  status.dataset.state = 'ready';
  status.textContent = matching.length > shown.length
    ? `${shown.length} van ${matching.length} plannen zichtbaar${recommendedOnly ? ' voor jou' : ''}`
    : `${matching.length} ${matching.length === 1 ? 'plan' : 'plannen'}${todayOnly ? ' vandaag' : ' in de agenda'}${recommendedOnly ? ' voor jou' : ''}`;
  const emptyMessage = recommendedOnly ? 'Geen sterke muziekmatches in deze selectie. Bekijk de volledige agenda.' : todayOnly ? 'Vandaag staat er niets in deze selectie. Bekijk de volledige agenda.' : 'Geen plannen gevonden. Probeer een andere zoekterm.';
  hasPrerenderedAgenda = false;
  agenda.dataset.prerendered = 'false';
  const content = document.createDocumentFragment();
  for (const [date, items] of Object.entries(groups)) {
    const day = element('section', 'day');
    const heading = element('div', 'day-heading');
    const title = element('h2');
    const renderedDate = new Date(`${date}T12:00:00`);
    const dateNode = element('time');
    dateNode.dateTime = date;
    dateNode.append(
      document.createTextNode(dateFormat.format(renderedDate)),
      element('span', 'day-year', date.slice(0, 4)),
    );
    title.append(dateNode);
    heading.append(title, element('span', '', `${items.length} ${items.length === 1 ? 'plan' : 'plannen'}`));
    const dayEvents = element('div', 'day-events');
    dayEvents.append(...items.sort(agendaOrder).map(eventElement));
    day.append(heading, dayEvents);
    content.append(day);
  }
  if (!matching.length) content.append(element('p', 'empty', emptyMessage));
  agenda.replaceChildren(content);
  syncLoadMore(shown.length, matching.length);
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

async function loadAgenda() {
  try {
  const fallbackEvents = JSON.parse(document.querySelector('#event-data').textContent);
  if (!Array.isArray(fallbackEvents)) throw new TypeError('Event fallback must be an array');
  let events = fallbackEvents.map(normalizeEvent).filter(Boolean);
  if (!events.length) throw new TypeError('Event fallback is empty');
  populateDateFilters(events);
  applyUrlFilters(events);
  const refreshSummary = () => updateAgendaSummary(events);
  if ('requestIdleCallback' in window) window.requestIdleCallback(refreshSummary, { timeout: 2_000 });
  else window.setTimeout(refreshSummary, 0);
  render(events);
  loadMoreButton?.addEventListener('click', () => {
    visibleLimit += PAGE_SIZE;
    hasPrerenderedAgenda = false;
    render(events);
  });
  agenda.addEventListener('click', event => {
    const button = event.target.closest('[data-event-calendar]');
    if (button) {
      downloadEvent(JSON.parse(button.dataset.eventCalendar));
      return;
    }
    const shareButton = event.target.closest('[data-event-share]');
    if (shareButton) shareEvent(JSON.parse(shareButton.dataset.eventShare), shareButton);
  });
  document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
    if (button.dataset.filter === 'all') selectedSources.clear();
    else if (selectedSources.has(button.dataset.filter)) selectedSources.delete(button.dataset.filter);
    else selectedSources.add(button.dataset.filter);
    filter = selectedSources.size === 1 ? [...selectedSources][0] : 'all';
    document.querySelectorAll('[data-filter]').forEach(control => {
      const active = control.dataset.filter === 'all' ? selectedSources.size === 0 : selectedSources.has(control.dataset.filter);
      control.classList.toggle('active', active);
      control.setAttribute('aria-pressed', String(active));
    });
    visibleLimit = PAGE_SIZE; render(events);
    syncFiltersToUrl();
  }));
  document.querySelector('[data-today-filter]').addEventListener('click', event => {
    todayOnly = !todayOnly;
    visibleLimit = PAGE_SIZE;
    event.currentTarget.classList.toggle('active', todayOnly);
    event.currentTarget.setAttribute('aria-pressed', String(todayOnly));
    render(events);
    syncFiltersToUrl();
  });
  document.querySelector('[data-recommended-filter]').addEventListener('click', event => {
    recommendedOnly = !recommendedOnly;
    visibleLimit = PAGE_SIZE;
    event.currentTarget.classList.toggle('active', recommendedOnly);
    event.currentTarget.setAttribute('aria-pressed', String(recommendedOnly));
    render(events);
    syncFiltersToUrl();
  });
  const updateSearch = event => {
    query = event.target.value.toLowerCase();
    visibleLimit = PAGE_SIZE;
    render(events);
    syncFiltersToUrl();
  };
  search.addEventListener('input', updateSearch);
  // Safari's native clear affordance on a search field can emit only `search`.
  search.addEventListener('search', updateSearch);
  monthFilter.addEventListener('change', event => {
    selectedMonth = event.target.value;
    if (selectedMonth) { selectedYear = selectedMonth.slice(0, 4); yearFilter.value = selectedYear; }
    visibleLimit = PAGE_SIZE;
    render(events);
    syncFiltersToUrl();
  });
  yearFilter.addEventListener('change', event => {
    selectedYear = event.target.value;
    if (selectedMonth && !selectedMonth.startsWith(`${selectedYear}-`)) { selectedMonth = ''; monthFilter.value = ''; }
    visibleLimit = PAGE_SIZE;
    render(events);
    syncFiltersToUrl();
  });
  dateFilter.addEventListener('change', event => { selectedDate = event.target.value; visibleLimit = PAGE_SIZE; render(events); syncFiltersToUrl(); });
  cityFilter.addEventListener('change', event => { selectedCity = event.target.value; visibleLimit = PAGE_SIZE; render(events); syncFiltersToUrl(); });
  typeFilter.addEventListener('input', event => { selectedType = event.target.value.toLowerCase(); visibleLimit = PAGE_SIZE; render(events); syncFiltersToUrl(); });
  window.addEventListener('popstate', () => {
    applyUrlFilters(events);
    visibleLimit = PAGE_SIZE;
    render(events);
  });
  const loadFullFeed = async () => {
    try {
      const response = await fetch('/events.json', { cache: 'no-cache', credentials: 'same-origin' });
      if (!response.ok) throw new Error('Event feed unavailable');
      const parsedEvents = await response.json();
      if (!Array.isArray(parsedEvents)) throw new TypeError('Event feed must be an array');
      const fullEvents = parsedEvents.map(normalizeEvent).filter(Boolean);
      if (!fullEvents.length) throw new TypeError('Event feed is empty');
      events = fullEvents;
      populateDateFilters(events);
      applyUrlFilters(events);
      updateAgendaSummary(events);
      render(events);
    } catch {
      // The server-rendered first page remains fully usable when the full feed
      // is unavailable; network status continues to explain offline state.
    }
  };
  if (location.protocol !== 'file:') {
    if ('requestIdleCallback' in window) window.requestIdleCallback(loadFullFeed, { timeout: 4_000 });
    else window.setTimeout(loadFullFeed, 1_000);
  }
  } catch {
    showStatusError('De agenda kon niet worden geladen.');
  }
}

loadAgenda();

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
    navigator.serviceWorker.register('/sw.js?v=20260811-9', { scope: '/' }).catch(() => {
      // The agenda remains fully usable online when service workers are unavailable.
    });
  });
}
