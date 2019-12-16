const path = require('path')
const Dotenv = require('dotenv-webpack')

const verifierConfig = {
  entry: './src/clients/certification/certificate-verifier/verifier.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'verifier.bundle.js',
    library: 'verifier'
  },
  plugins: [
    new Dotenv({
      path: './.env.local',
    }),
  ],
}

const certifierConfig = {
  entry: './src/clients/certification/certificate-certifier/certifier.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'certifier.bundle.js',
    library: 'certifier'
  },
  plugins: [
    new Dotenv({
      path: './.env.local',
    }),
  ],
}

module.exports = [
  verifierConfig,
  certifierConfig,
]
