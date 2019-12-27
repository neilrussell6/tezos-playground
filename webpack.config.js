const path = require('path')
const Dotenv = require('dotenv-webpack')

const plugins = [
  new Dotenv({
    path: './.env',
  }),
]

const node = {
  fs: 'empty'
}

const eztzVerifierConfig = {
  entry: './src/clients/eztz/certification/certificate-verifier/verifier.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'eztz-verifier.bundle.js',
    library: 'eztzVerifier'
  },
  plugins,
  node,
}

const eztzCertifierConfig = {
  entry: './src/clients/eztz/certification/certificate-certifier/certifier.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'eztz-certifier.bundle.js',
    library: 'eztzCertifier'
  },
  plugins,
  node,
}

const conseiljsVerifierConfig = {
  entry: './src/clients/conseiljs/certification/certificate-verifier/verifier.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'conseiljs-verifier.bundle.js',
    library: 'conseiljsVerifier'
  },
  plugins,
  node,
}

const conseiljsCertifierConfig = {
  entry: './src/clients/conseiljs/certification/certificate-certifier/certifier.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'conseiljs-certifier.bundle.js',
    library: 'conseiljsCertifier'
  },
  plugins,
  node,
}

const conseiljsSandboxConfig = {
  entry: './src/clients/conseiljs/sandbox/sandbox.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'conseiljs-sandbox.bundle.js',
    library: 'conseiljsSandbox'
  },
  plugins,
  node,
}

module.exports = [
  eztzVerifierConfig,
  eztzCertifierConfig,
  conseiljsVerifierConfig,
  conseiljsCertifierConfig,
  conseiljsSandboxConfig,
]
