self.addEventListener('install', (event) => {
    event.waitUntil(
      caches.open('my-cache').then((cache) => {
        return cache.addAll([
          '/',
          '/base.html',
          '/static/css/index.css',
          '/static/css/eggy.css',
          '/static/css/progressbar.css',
          '/static/css/theme.css',
          '/static/js/index.js',
          '/static/font/Vazirmatn-Black.woff2',
          '/static/font/Vazirmatn-Bold.woff2',
          '/static/font/Vazirmatn-ExtraBlack.woff2',
          '/static/js/index.js',
          '/static/js/eggy.js',
          '/static/covers/img/1.png',
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', (event) => {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request);
      })
    );
  });