const CACHE_PREFIX = 'uit-vandaag-';
const STATIC_CACHE = `${CACHE_PREFIX}static-20260802-26`;
const RUNTIME_CACHE = `${CACHE_PREFIX}runtime-20260802-27`;

const APP_SHELL = [
  '/',
  '/index.html',
  '/about.html',
  '/disclaimer.html',
  '/privacy.html',
  '/styles.css?v=20260802-17',
  '/app.js?v=20260802-14',
  '/back-to-top.js?v=20260802-2',
  '/analytics-consent.js?v=20260802-2',
  '/theme.js?v=20260802-3',
  '/loading-watchdog.js?v=20260801-1',
  '/site.webmanifest',
  '/events.json',
  '/events.ics',
  '/favicon.ico',
  '/assets/favicon-32.png',
  '/assets/apple-touch-icon.png',
  '/assets/icon-96.webp',
  '/assets/icon-192.webp',
  '/assets/icon-192.png',
  '/assets/icon-512.png',
  '/assets/icon-maskable-512.png',
  '/assets/fonts/archivo-narrow-latin.woff2',
  '/assets/fonts/dm-mono-400-latin.woff2',
  '/assets/fonts/dm-mono-500-latin.woff2',
  '/assets/logo-metropool.svg',
  '/assets/logo-de-cactus.png',
  '/assets/logo-fc-twente.svg',
  '/assets/logo-oogst.svg',
  '/assets/logo-uit-in-hengelo.svg',
  '/assets/venues/metropool-640.webp',
  '/assets/venues/de-cactus-640.webp',
  '/assets/venues/oogst-640.webp',
  '/assets/venues/uit-in-hengelo-640.webp',
  '/assets/venues/grolsch-veste-640.webp',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys
        .filter(key => key.startsWith(CACHE_PREFIX) && ![STATIC_CACHE, RUNTIME_CACHE].includes(key))
        .map(key => caches.delete(key))))
      .then(() => self.clients.claim()),
  );
});

async function networkFirst(request, fallbackUrl) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(RUNTIME_CACHE);
      await cache.put(request, response.clone());
      return response;
    }
    const cached = await latestCachedResponse(request);
    return cached || (fallbackUrl && await latestCachedResponse(fallbackUrl)) || response;
  } catch {
    return await latestCachedResponse(request)
      || (fallbackUrl && await latestCachedResponse(fallbackUrl))
      || Response.error();
  }
}

async function latestCachedResponse(request) {
  const runtime = await caches.open(RUNTIME_CACHE);
  return await runtime.match(request) || await caches.match(request);
}

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  if (response.ok) {
    const cache = await caches.open(RUNTIME_CACHE);
    await cache.put(request, response.clone());
  }
  return response;
}

self.addEventListener('fetch', event => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin || url.pathname.startsWith('/api/')) return;

  if (request.mode === 'navigate') {
    event.respondWith(networkFirst(request, '/'));
    return;
  }
  if (['/events.json', '/events.ics'].includes(url.pathname)) {
    event.respondWith(networkFirst(request));
    return;
  }
  event.respondWith(cacheFirst(request));
});
