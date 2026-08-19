(() => {
  const FORECAST_URL = 'https://api.open-meteo.com/v1/forecast?latitude=52.2658&longitude=6.7931&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=Europe%2FAmsterdam&forecast_days=16';
  const WEATHER_CODES = {
    0: ['☀️', 'zonnig'],
    1: ['🌤️', 'overwegend zonnig'],
    2: ['⛅', 'half bewolkt'],
    3: ['☁️', 'bewolkt'],
    45: ['🌫️', 'mistig'],
    48: ['🌫️', 'mistig'],
    51: ['🌦️', 'druilerig'],
    53: ['🌦️', 'druilerig'],
    55: ['🌦️', 'druilerig'],
    56: ['🌧️', 'ijzel'],
    57: ['🌧️', 'ijzel'],
    61: ['🌧️', 'regen'],
    63: ['🌧️', 'regen'],
    65: ['🌧️', 'stevige regen'],
    66: ['🌧️', 'ijzel'],
    67: ['🌧️', 'ijzel'],
    71: ['🌨️', 'sneeuw'],
    73: ['🌨️', 'sneeuw'],
    75: ['❄️', 'hevige sneeuw'],
    77: ['🌨️', 'sneeuwkorrels'],
    80: ['🌦️', 'buien'],
    81: ['🌧️', 'regenbuien'],
    82: ['⛈️', 'zware buien'],
    85: ['🌨️', 'sneeuwbuien'],
    86: ['🌨️', 'sneeuwbuien'],
    95: ['⛈️', 'onweer'],
    96: ['⛈️', 'onweer'],
    99: ['⛈️', 'zwaar onweer'],
  };

  let forecastByDate = null;

  async function loadForecast() {
    try {
      const response = await fetch(FORECAST_URL, { cache: 'no-store' });
      if (!response.ok) return;
      const data = await response.json();
      const times = data?.daily?.time || [];
      const codes = data?.daily?.weather_code || [];
      const highs = data?.daily?.temperature_2m_max || [];
      const rain = data?.daily?.precipitation_probability_max || [];
      const next = {};
      for (let i = 0; i < times.length; i++) {
        next[times[i]] = { code: codes[i], high: highs[i], rain: rain[i] };
      }
      forecastByDate = next;
      applyWeather();
    } catch {
      // Weather is an optional enhancement; the agenda stays fully usable without it.
    }
  }

  function format(entry) {
    const [icon, label] = WEATHER_CODES[entry.code] || ['🌡️', 'wisselend'];
    const high = Math.round(entry.high);
    const rainNote = entry.rain >= 60 ? ` · ${Math.round(entry.rain)}% regen` : '';
    return `${icon} ${high}°${rainNote} · ${label}`;
  }

  function applyWeather() {
    if (!forecastByDate) return;
    document.querySelectorAll('.day-heading').forEach(heading => {
      const time = heading.querySelector('time[datetime]');
      if (!time) return;
      const date = time.getAttribute('datetime').slice(0, 10);
      const entry = forecastByDate[date];
      const existing = heading.querySelector('.day-weather');
      if (!entry) {
        existing?.remove();
        return;
      }
      if (!existing) heading.append(Object.assign(document.createElement('p'), { className: 'day-weather' }));
      heading.querySelector('.day-weather').textContent = format(entry);
    });
  }

  function init() {
    document.addEventListener('uitagenda:rendered', applyWeather);
    loadForecast();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();