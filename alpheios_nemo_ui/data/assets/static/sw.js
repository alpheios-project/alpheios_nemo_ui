/* global self, workbox, Response, URL */
console.log('Service worker has been registered')

self.importScripts('/workbox/workbox-sw.js');

self.addEventListener('install', event => {
  console.log(`Service worker install event`)
})

self.addEventListener('activate', event => {
  console.log(`Service worker activate event`)
})

// This code runs whenever a Service Worker script is loaded, and Workbox library is loaded too
if (workbox) {
  console.log(`workbox is active`)
  // workbox.core.setLogLevel(workbox.core.LOG_LEVELS.debug)

  self.addEventListener('fetch', evt => {
    console.log(`Service worker fetch evt: ${evt.request.url}`, evt)
  })

  // Will it cause an error if overwrite current cache files as with Cache.addAll()?
  self.__precacheManifest = [].concat(self.__precacheManifest || [])
  workbox.precaching.precacheAndRoute(
    self.__precacheManifest
  )


  // Texts
  workbox.routing.registerRoute(
    /.*\/text\/.*/,
    new workbox.strategies.CacheFirst({
      cacheName: 'alpheios-text-resources',
      plugins: [
        new workbox.cacheableResponse.Plugin({
          statuses: [200],
        }),
        new workbox.expiration.Plugin({
          maxAgeSeconds: 60 * 60 * 24 * 365, // One year
          maxEntries: 30,
        })
      ]
    })
  )

  // Collections
  workbox.routing.registerRoute(
    /.*\/collections\/.*/,
    new workbox.strategies.CacheFirst({
      cacheName: 'alpheios-collection-resources',
      plugins: [
        new workbox.cacheableResponse.Plugin({
          statuses: [200],
        }),
        new workbox.expiration.Plugin({
          maxAgeSeconds: 60 * 60 * 24 * 365, // One year
          maxEntries: 30,
        })
      ]
    })
  )

  // Grammar resources
  workbox.routing.registerRoute(
    /(?:https?:\/\/grammars\.alpheios\.net)\/.*/,
    new workbox.strategies.CacheFirst({
      cacheName: 'alpheios-grammar-resources',
      plugins: [
        new workbox.cacheableResponse.Plugin({
          statuses: [200],
        }),
        new workbox.expiration.Plugin({
          maxAgeSeconds: 60 * 60 * 24 * 365, // One year
          maxEntries: 30,
        })
      ]
    })
  )

  // JavaScript files
  workbox.routing.registerRoute(
    /.*\.(?:js[^on]).*/,
    // Use the cache if it's available
    new workbox.strategies.StaleWhileRevalidate({
      // Use a custom cache name
      cacheName: 'alpheios-js'
    })
  )

  // CSS files
  workbox.routing.registerRoute(
    /.*\.(?:css).*/,
    // Use the cache if it's available
    new workbox.strategies.StaleWhileRevalidate({
      // Use a custom cache name
      cacheName: 'alpheios-css'
    })
  )

  // Image files
  workbox.routing.registerRoute(
    /.*\.(?:png|jpg|jpeg|svg|gif).*/,
    // Use the cache if it's available
    new workbox.strategies.StaleWhileRevalidate({
      // Use a custom cache name
      cacheName: 'alpheios-images',
      plugins: [
        new workbox.expiration.Plugin({
          maxEntries: 60,
          maxAgeSeconds: 30 * 24 * 60 * 60, // 30 Days
        })
      ]
    })
  )

  // Cache the Google Fonts stylesheets with a stale-while-revalidate strategy.
  workbox.routing.registerRoute(
    /^https:\/\/fonts\.googleapis\.com/,
    new workbox.strategies.StaleWhileRevalidate({
      cacheName: 'google-fonts-stylesheets',
    })
  )

// Cache the underlying font files with a cache-first strategy for 1 year.
  workbox.routing.registerRoute(
    /^https:\/\/fonts\.gstatic\.com/,
    new workbox.strategies.CacheFirst({
      cacheName: 'google-fonts-webfonts',
      plugins: [
        new workbox.cacheableResponse.Plugin({
          statuses: [0, 200],
        }),
        new workbox.expiration.Plugin({
          maxAgeSeconds: 60 * 60 * 24 * 365, // One year
          maxEntries: 30,
        })
      ]
    })
  )

  // All other resources
  workbox.routing.registerRoute(
    /(?:https?:\/\/).*/,
    new workbox.strategies.StaleWhileRevalidate({
      cacheName: 'alpheios-other-resources'
    })
  )

  // Error handler
  workbox.routing.setCatchHandler(({url, event, params}) => {
    console.log(`Workbox routing failed:`, url, event, params)
  })
} else {
  console.log(`workbox global is not available, workbox has probably not been loaded`)
}

self.addEventListener('message', (event) => {
  if (!event.data) {
    return
  }

  switch (event.data) {
    case 'skipWaiting':
      self.skipWaiting()
      break
    default:
      // NOOP
      break
  }
})

if ('storage' in navigator && 'estimate' in navigator.storage) {
  navigator.storage.estimate().then(({usage, quota}) => {
    console.log(`Using ${usage} out of ${quota} bytes (${Math.round(usage / quota * 100)} %).`)
  }).catch(error => {
    console.error('Loading storage estimate failed:')
    console.log(error.stack)
  })
} else {
  console.error('navigator.storage.estimate API unavailable.')
}
