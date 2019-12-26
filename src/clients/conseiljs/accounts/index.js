const conseiljs = require('conseiljs')
const util = require('util')
const serverInfo = {
  url: 'https://conseil-dev.cryptonomic-infra.tech:443',
  apiKey: 'b9labs',
}

async function listPlatforms() {
  const platforms = await conseiljs.ConseilMetadataClient.getPlatforms(serverInfo)
  console.log(`${util.inspect(platforms, false, 2, false)}`)
}

listPlatforms()
