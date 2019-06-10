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

  workbox.routing.registerRoute(
    // Cache image files
    /.*\.(?:png|jpg|jpeg|svg|gif)/,
    // Use the cache if it's available
    new workbox.strategies.StaleWhileRevalidate({
      // Use a custom cache name
      cacheName: 'image-cache',
      plugins: [
        new workbox.expiration.Plugin({
          // Cache only 20 images
          maxEntries: 20,
          // Cache for a maximum of a week
          maxAgeSeconds: 7 * 24 * 60 * 60
        })
      ]
    })
  )

  // External resources
  workbox.routing.registerRoute(
    /(?:https?:\/\/).*/,
    new workbox.strategies.StaleWhileRevalidate({
      cacheName: 'external-resources-cache'
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
