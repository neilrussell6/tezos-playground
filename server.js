const { splitEvery, fromPairs, compose, propOr } = require('ramda')

// (1)
const connect = require('connect')
const serveStatic = require('serve-static')

// // (2)
// const finalhandler = require('finalhandler')
// const http = require('http')
// const serveStatic = require('serve-static')

// --------------------------
// server (1)
// --------------------------

const serve = config => connect()
  .use(serveStatic(__dirname))
  .listen(config.port, () => {
    console.log(`Server running on ${config.port}...`)
  })

// --------------------------
// server (2)
// --------------------------

// const serve = config => {
//   const route = serveStatic(__dirname)
//   const server = http.createServer((req, res) => {
//     route(req, res, finalhandler(req, res))
//   })
//   server.listen(config.port)
//   console.log(`Server running on ${config.port}...`)
// }

// --------------------------
// CLI
// --------------------------

const args = compose(fromPairs, splitEvery(2), x => x.slice(2))(process.argv)
const config = {
  port: propOr('8080', '-p', args)
}

serve(config)
