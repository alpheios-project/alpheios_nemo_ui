const projectRoot = process.cwd()

const webpack = {
  common: {
    entry: './dummy.js',
    output: {
      path: projectRoot
    },
    externals: { }
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
