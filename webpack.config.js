const path = require('path')
const Dotenv = require('dotenv-webpack')

const certificationConfig = {
  entry: './src/clients/certification/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'certification.bundle.js',
    library: 'certification'
  },
  plugins: [
    new Dotenv({
      path: './.env.local',
    }),
  ],
}

module.exports = [
  certificationConfig,
]
