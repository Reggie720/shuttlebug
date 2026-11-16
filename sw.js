const RELEASE = '49d0a83142d0';
const CACHE = 'shuttlebug-' + RELEASE;
const SHELL = ['/', '/index.html', `/styles.css?v=${RELEASE}`, `/app.js?v=${RELEASE}`, `/catalog.js?v=${RELEASE}`, '/manifest.json', '/icons/icon-192.png', '/icons/icon-512.png', '/icons/maskable-512.png', '/icons/apple-touch-icon.png', '/icons/icon.svg'];
const SHELL_PATHS = new Set(SHELL.map(path => new URL(path, self.location.origin).pathname));
self.addEventListener('install', event => event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(SHELL.map(path => new Request(path, {cache:'reload'})))).then(() => self.skipWaiting())));
self.addEventListener('activate', event => event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith('shuttlebug-') && key !== CACHE).map(key => caches.delete(key)))).then(() => self.clients.claim())));
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  // Cache only the app shell. Never cache media, ads, ranges or publisher config.
  if (event.request.method !== 'GET' || url.origin !== self.location.origin || event.request.headers.has('range') || !SHELL_PATHS.has(url.pathname)) return;
  event.respondWith(fetch(event.request, {cache:'no-cache'}).then(response => {
    if (response.ok) { const copy = response.clone(); event.waitUntil(caches.open(CACHE).then(cache => cache.put(event.request, copy))); }
    return response;
  }).catch(async () => (await caches.match(event.request)) || (event.request.mode === 'navigate' ? caches.match('/') : Response.error())));
});
