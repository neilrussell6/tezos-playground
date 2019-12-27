// This is for demonstration purposes only! Don't handle live keys like this.
// You can hardcode your account settings and contract address here for local testing.
function initUI() {
  updateUISetting({
    provider: process.env.BABYLONNET_URL,
    apiKey: process.env.CONSEIL_API_KEY,
    mnemonic: process.env.CERTIFICATION_CONTRACT_OWNER_MNEMONIC,
    password: process.env.CERTIFICATION_CONTRACT_OWNER_PASSWORD,
    email: process.env.CERTIFICATION_CONTRACT_OWNER_EMAIL,
    contractAddress: process.env.CERTIFICATION_CONTRACT_ADDRESS,
  })
  // setup all UI actions
  $('#btn_issue').click(() => certify($('#inp_address').val(), $('#inp_name').val()))
  $('#btn_revoke').click(() => revoke($('#inp_address2').val()))
  $('#btn_settings').click(() => $('#settings-box').toggle())
  $("#upl_input").on("change", loadJsonFile)
  $('#btn_load').click(() => $("#upl_input").click())
}

function updateUISetting(accountSettings) {
  $('#provider').val(accountSettings.provider)
  $('#apiKey').val(accountSettings.apiKey)
  $('#mnemonic').val(accountSettings.mnemonic)
  $('#password').val(accountSettings.password)
  $('#email').val(accountSettings.email)
  $('#contractAddress').val(accountSettings.contractAddress)
}

function readUISettings() {
  return {
    provider: $('#provider').val(),
    apiKey: $('#apiKey').val(),
    mnemonic: $('#mnemonic').val(),
    password: $('#password').val(),
    email: $('#email').val(),
    contractAddress: $('#contractAddress').val()
  }
}

function loadJsonFile() {
  // This doesn't work in IE
  const file = $("#upl_input").get(0).files[0]
  const reader = new FileReader()
  const accountSettings = readUISettings()
  reader.onload = parseFaucetJson(accountSettings)
  reader.onloadend = () => updateUISetting(accountSettings)
  reader.readAsText(file)
}

// Parses the faucet json file
function parseFaucetJson(settingsToFillIn) {
  return function (evnt) {
    const parsed = JSON.parse(evnt.target.result)
    settingsToFillIn.mnemonic = parsed['mnemonic'].join(" ")
    settingsToFillIn.password = parsed['password']
    settingsToFillIn.email = parsed['email']
    return settingsToFillIn
  }
}

function reportResult(result, type, itemSelector) {
  return $(itemSelector)
    .html(result)
    .removeClass()
    .addClass("result-bar")
    .addClass(type == "error"
              ? "result-false"
              : type == "ok"
                ? "result-true"
                : "result-load")
}

async function certify(studentAddress, studentName) {

  const accountSettings = readUISettings()

  // --------------------------
  // keys
  // --------------------------

  const keys = await conseiljs.TezosWalletUtil.unlockFundraiserIdentity(
    accountSettings.mnemonic,
    accountSettings.email,
    accountSettings.password,
    accountSettings.pkh
  )

  // --------------------------
  // entry points
  // --------------------------

  const contractParameters = 'parameter (or (pair %certify (address %address) (string %name)) (address %revoke));'
  const entryPoints = await conseiljs.TezosContractIntrospector.generateEntryPointsFromParams(contractParameters)
  console.log(entryPoints)
  entryPoints.forEach(p => {
    console.log(`${p.name}(${p.parameters.map(pp => (pp.name || 'unnamed') + '/' + pp.type).join(', ')})`)
  })
  console.log('################################ entrypoints')
  console.log('certify: ', entryPoints[0].generateParameter('ADDRESS', 'NAME'))
  console.log('revoke: ', entryPoints[1].generateParameter('ADDRESS'))

  // --------------------------
  // transaction
  // --------------------------

  const request = '(Left (Pair "' + studentAddress + '" "' + studentName + '" ))'

  reportResult("Sending...", "info", "#result-bar")
  console.log('tezosNodeUrl', accountSettings.provider)
  console.log('keyStore', keys)
  console.log('toAddress', accountSettings.contractAddress)
  console.log('amount', 0)
  console.log('operationFee', 100000)
  console.log('derivationPath', '')
  console.log('storageLimit', 1000)
  console.log('gasLimit', 100000)
  console.log('entrypoint', undefined)
  console.log('parameters', request)
  console.log('parameterFormat', conseiljs.TezosParameterFormat.Michelson)
  try {
    const result = await conseiljs.TezosNodeWriter.sendContractInvocationOperation(
      accountSettings.provider,
      keys,
      accountSettings.contractAddress,
      0,
      100000,
      '',
      1000,
      100000,
      undefined,
      request,
      conseiljs.TezosParameterFormat.Michelson,
    )

    console.table(result)

    return reportResult(
      $("<a>").html("Op Hash: " + result["operationGroupID"]).attr("href", "https://better-call.dev/babylon/" + result["operationGroupID"].split('"')[1]),
      "ok",
      "#result-bar"
    )

  } catch(e) {
    console.log(e)
    return reportResult("Error: " + e.error, "error", "#result-bar")
  }
}

async function revoke(studentAddress) {

  const accountSettings = readUISettings()

  // --------------------------
  // keys
  // --------------------------

  const keys = await conseiljs.TezosWalletUtil.unlockFundraiserIdentity(
    accountSettings.mnemonic,
    accountSettings.email,
    accountSettings.password,
    accountSettings.pkh
  )

  // --------------------------
  // entry points
  // --------------------------

  const contractParameters = 'parameter (or (pair %certify (address %address) (string %name)) (address %revoke));'
  const entryPoints = await conseiljs.TezosContractIntrospector.generateEntryPointsFromParams(contractParameters)
  console.log(entryPoints)
  entryPoints.forEach(p => {
    console.log(`${p.name}(${p.parameters.map(pp => (pp.name || 'unnamed') + '/' + pp.type).join(', ')})`)
  })
  console.log('################################ entrypoints')
  console.log('certify: ', entryPoints[0].generateParameter('ADDRESS', 'NAME'))
  console.log('revoke: ', entryPoints[1].generateParameter('ADDRESS'))

  // --------------------------
  // transaction
  // --------------------------

  const request = '(Right "' + studentAddress + '")'

  reportResult("Sending...", "info", "#result-bar2")
  console.log('tezosNodeUrl', accountSettings.provider)
  console.log('keyStore', keys)
  console.log('toAddress', accountSettings.contractAddress)
  console.log('amount', 0)
  console.log('operationFee', 100000)
  console.log('derivationPath', '')
  console.log('storageLimit', 1000)
  console.log('gasLimit', 100000)
  console.log('entrypoint', undefined)
  console.log('parameters', request)
  console.log('parameterFormat', conseiljs.TezosParameterFormat.Michelson)
  try {
    const result = await conseiljs.TezosNodeWriter.sendContractInvocationOperation(
      accountSettings.provider,
      keys,
      accountSettings.contractAddress,
      0,
      100000,
      '',
      1000,
      100000,
      undefined,
      request,
      conseiljs.TezosParameterFormat.Michelson,
    )

    console.table(result)

    return reportResult(
      $("<a>").html("Op Hash: " + result["operationGroupID"]).attr("href", "https://better-call.dev/babylon/" + result["operationGroupID"].split('"')[1]),
      "ok",
      "#result-bar2"
    )

  } catch(e) {
    console.log(e)
    return reportResult("Error: " + e.error, "error", "#result-bar2")
  }
}

$(document).ready(initUI)
