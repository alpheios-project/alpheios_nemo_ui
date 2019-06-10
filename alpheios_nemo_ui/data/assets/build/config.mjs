import VueLoaderPlugin from '../node_modules/vue-loader/lib/plugin.js'
import InjectManifest from '../node_modules/workbox-webpack-plugin/build/inject-manifest.js'
import WebpackPwaManifest from 'webpack-pwa-manifest'
import HtmlWebpackPlugin from 'html-webpack-plugin'
import Package from '../package.json'

import path from 'path'
const projectRoot = process.cwd()

const sharedManifestConf = {
  name: 'My Progressive Web App',
  short_name: 'MyPWA',
  description: 'My awesome Progressive Web App!',
  background_color: '#ffffff',
  fingerprints: false,
  inject: false,
  ios: {
    'apple-mobile-web-app-title': 'Alpheios Reader',
    'apple-mobile-web-app-status-bar-style': '#73CDDE'
  },
  icons: [
    {
      src: path.resolve('images/alpheios_32.png'),
      sizes: [36, 48, 72, 96, 144, 192, 512],
      destination: path.join('alpheios_nemo-ui/data/assets/images/icons', 'pwa')
    },
    {
      src: path.resolve('images/alpheios_32.png'),
      sizes: [120, 152, 167, 180, 1024],
      destination: path.join('alpheios_nemo-ui/data/assets/images/icons', 'ios'),
      ios: true
    }
  ]
}

const webpack = {
  common: {
    entry: './dummy.js',
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
