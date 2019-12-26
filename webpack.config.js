const path = require('path')
const Dotenv = require('dotenv-webpack')

const plugins = [
  new Dotenv({
    path: './.env',
  }),
]

const eztzVerifierConfig = {
  entry: './src/clients/eztz/certification/certificate-verifier/verifier.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'eztz-verifier.bundle.js',
    library: 'eztzVerifier'
  },
  plugins,
}

const eztzCertifierConfig = {
  entry: './src/clients/eztz/certification/certificate-certifier/certifier.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'eztz-certifier.bundle.js',
    library: 'eztzCertifier'
  },
  plugins,
}

const conseiljsVerifierConfig = {
  entry: './src/clients/conseiljs/certification/certificate-verifier/verifier.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'conseiljs-verifier.bundle.js',
    library: 'conseiljsVerifier'
  },
  plugins,
}

const conseiljsCertifierConfig = {
  entry: './src/clients/conseiljs/certification/certificate-certifier/certifier.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'conseiljs-certifier.bundle.js',
    library: 'conseiljsCertifier'
  },
  plugins,
}

module.exports = [
  eztzVerifierConfig,
  eztzCertifierConfig,
  conseiljsVerifierConfig,
  conseiljsCertifierConfig,
]
