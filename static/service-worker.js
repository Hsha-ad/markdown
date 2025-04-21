// service-worker.js
const CACHE_NAME = 'netdisk-assistant-cache-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/script.js',
    '/static/js/error-handler.js'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
           .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
           .then(response => {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.filter(cacheName => cacheName!== CACHE_NAME)
                   .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});