import WebpackPwaManifest from 'webpack-pwa-manifest'
import path from 'path'
const projectRoot = process.cwd()

const sharedManifestConf = {
  name: 'Alpheios Reader progressive webapp',
  short_name: 'Alpheios Reader PWA',
  description: 'An Alpheios Reader progressive web application',
  theme_color: "#0E2233",
  background_color: "#BCE5F0",
  display: "standalone",
  orientation: "portrait",
  scope: "/",
  start_url: "/",
  fingerprints: false,
  inject: false,
  ios: {
    'apple-mobile-web-app-title': 'Alpheios Reader',
    'apple-mobile-web-app-status-bar-style': '#73CDDE'
  },
  icons: [
    {
      src: path.resolve('images/logo.png'),
      sizes: [36, 48, 72, 96, 144, 192, 512],
      destination: path.join('images/icons', 'pwa')
    },
    {
      src: path.resolve('images/logo.png'),
      sizes: [120, 152, 167, 180, 1024],
      destination: path.join('images/icons', 'ios'),
      ios: true
    }
  ]
}

const webpack = {
  common: {
    entry: './dummy.js',
    output: {
      path: projectRoot
    },
    externals: { },
    plugins: [
      new WebpackPwaManifest(sharedManifestConf)
    ]
  },

  production: {
    mode: 'production',
    output: {filename: 'app.min.js'},
    plugins: [
    ]
  },

  development: {
    mode: 'development',
    output: {filename: 'app.js'},
    plugins: [
    ]
  }
}

const sass = {
  tasks: [
    { source: `scss/alpheios.scss`,
      target: `css/alpheios.css`,
      style: 'compressed',
      sourceMap: true
    }
  ]
}

export { webpack, sass }
