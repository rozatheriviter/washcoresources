/**
 * SERVICE WORKER - Rooted: WashCo
 *
 * Handles offline capabilities and caching.
 *
 * IMPORTANT: When you update any file (HTML, CSS, JS, or images),
 * you MUST increment the 'vX' number in CACHE_NAME below.
 * This tells the browser to clear the old cache and download the new files.
 */

const CACHE_NAME = 'rooted-washco-v8';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './map.html',
  './about.html',
  './submit-resource.html',
  './style.css',
  './app.js',
  './map.js',
  './resources.js',
  './transit_data.js',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS_TO_CACHE))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

/**
 * FETCH STRATEGY: Stale-While-Revalidate
 * 1. Checks cache for a match.
 * 2. Returns the cached version immediately (if found) for speed.
 * 3. Simultaneously fetches the latest version from the network
 *    and updates the cache for the next visit.
 */
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        const fetchPromise = fetch(event.request).then(networkResponse => {
          if (networkResponse && networkResponse.ok) {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(event.request, responseToCache);
            });
          }
          return networkResponse;
        }).catch(() => {
          // If fetch fails, we just return the cached response (which we're already doing via the outer promise)
        });

        return cachedResponse || fetchPromise;
      })
  );
});
