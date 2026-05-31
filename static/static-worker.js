self.addEventListener('install', (event) => {
    console.log('Service Worker telepítve');
});

self.addEventListener('fetch', (event) => {
    event.respondWith(fetch(event.request));
});