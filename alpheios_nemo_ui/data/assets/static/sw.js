console.log('Hello from sw.js');

importScripts('https://storage.googleapis.com/workbox-cdn/releases/3.2.0/workbox-sw.js');

if (workbox) {
  console.log(`Yay! Workbox is loaded 🎉`);
  self.addEventListener('fetch', evt => {
    console.log(`Service worker fetch evt: ${evt.request.url}`, evt)
    if (evt.request.url.match(/.+dynamic.+/)) {
      console.log(`This is a content page request`)
      let response = self.fetch(evt.request).then(function (response) {
        console.log(`Response received: `, response)
        return response.text()
      }).then(function (data) {
        if (!(/meta name="viewport"/.test(data))) {
          // Set initial viewport size and scaling if not set by the page to prevent Alpheios elements to have wrong size
          data = data.replace(`<head>`, `<head>` + viewportMeta)
        }

        return new Response(data, {
          headers: {'Content-Type': 'text/html'}
        })
      }).catch(function (err) {
        console.log(`Fetch failed for ${evt.request.url}:`, err)
      })

      evt.respondWith(response)
    }
  })


  workbox.precaching.precacheAndRoute([
    {
      "url": "/",
      "revision": "2"
    }
  ]);

  workbox.routing.registerRoute(
    /\.(?:js|css)$/,
    workbox.strategies.staleWhileRevalidate({
      cacheName: 'static-resources',
    }),
  );

  workbox.routing.registerRoute(
    /text/,
    workbox.strategies.cacheFirst({
      cacheName: 'text-resources',
    }),
  );

  workbox.routing.registerRoute(
    /collections/,
    workbox.strategies.cacheFirst({
      cacheName: 'collection-resources',
    }),
  );


  workbox.routing.registerRoute(
    /\.(?:png|gif|jpg|jpeg|svg)$/,
    workbox.strategies.cacheFirst({
      cacheName: 'images',
      plugins: [
        new workbox.expiration.Plugin({
          maxEntries: 60,
          maxAgeSeconds: 30 * 24 * 60 * 60, // 30 Days
        }),
      ],
    }),
  );

  workbox.routing.registerRoute(
    new RegExp('https://fonts.(?:googleapis|gstatic).com/(.*)'),
    workbox.strategies.cacheFirst({
      cacheName: 'googleapis',
      plugins: [
        new workbox.expiration.Plugin({
          maxEntries: 30,
        }),
      ],
    }),
  );
} else {
  console.log(`Boo! Workbox didn't load 😬`);
}
