/* global self, workbox, Response, URL */
console.log('Service worker has been registered')
let swScriptURL
let clientsURL = []
let injectionStyles = ''
let injectionScripts = ''
let backToTocBtn = ''
let tocURL = ''
const viewportMeta = `<meta name="viewport" content="width=device-width, initial-scale=1">`

self.importScripts('/workbox/workbox-sw.js');

self.addEventListener('install', event => {
  console.log(`Service worker install event`)
  // Get a URL object for the service worker script's location.
  swScriptURL = new URL(self.location)

  // Get URL objects for each client's location.
  self.clients.matchAll({includeUncontrolled: true}).then(clients => {
    for (const client of clients) {
      console.log(`Clients are`)
      console.log(clients)
      const clientUrl = new URL(client.url)
      clientsURL.push(clientUrl)
      if (/.+index.*\.html$/.test(clientUrl.pathname)) {
        // This is most likely a TOC page
        tocURL = clientUrl.pathname
      }
    }
  })
})

self.addEventListener('activate', event => {
  console.log(`Service worker activate event`)
  console.log(`Service worker script URL is`, swScriptURL)
  console.log(clientsURL)
  // Parse precache manifest to determine what needs to be injected
  for (const resource of self.__precacheManifest) {
    if (/\.css$/.test(resource.url)) {
      injectionStyles += `<link href="/${resource.url}" rel="stylesheet">\n`
    }
    if (/\.js$/.test(resource.url)) {
      injectionScripts += `<script type="text/javascript" src="/${resource.url}"></script>\n`
    }
    backToTocBtn = `<a class="alpheios-pwa-content-toc-back-btn" data-alph-exclude-all-cpe="true" href="${tocURL}">Back to TOC</a>`
  }
})

// This code runs whenever a Service Worker script is loaded, and Workbox library is loaded too
if (workbox) {
  console.log(`workbox is active`)
  // workbox.core.setLogLevel(workbox.core.LOG_LEVELS.debug)

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
        data = data.replace(`</head>`, injectionStyles + `</head>`)
        data = data.replace(`<body>`, `<body>` + backToTocBtn)
        data = data.replace(`</body>`, injectionScripts + `</body>`)

        return new Response(data, {
          headers: {'Content-Type': 'text/html'}
        })
      }).catch(function (err) {
        console.log(`Fetch failed for ${evt.request.url}:`, err)
      })

      evt.respondWith(response)
    }
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
    workbox.strategies.staleWhileRevalidate({
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
    workbox.strategies.staleWhileRevalidate({
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
