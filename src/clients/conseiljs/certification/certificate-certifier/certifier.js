// This is for demonstration purposes only! Don't handle live keys like this.
// You can hardcode your account settings and contract address here for local testing.
function initUI() {
  updateUISetting({
    provider: process.env.CONSEIL_API_URL,
    apiKey: process.env.CONSEIL_API_KEY,
    mnemonic: process.env.CERTIFICATION_CONTRACT_OWNER_MNEMONIC,
    password: process.env.CERTIFICATION_CONTRACT_OWNER_PASSWORD,
    email: process.env.CERTIFICATION_CONTRACT_OWNER_EMAIL,
    contractAddress: process.env.CERTIFICATION_CONTRACT_ADDRESS,
  })
  // setup all UI actions
  $('#btn_issue').click(() => certify($('#inp_address').val(), $('#inp_name').val()))
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

// This is the main function, interacting with the contract through eztz
async function certify(studentAddress, studentName) {

  const accountSettings = readUISettings()

  const serverInfo = {
    url: accountSettings.provider,
    apiKey: accountSettings.apiKey,
  }

  const keys = await conseiljs.TezosWalletUtil.unlockFundraiserIdentity(
    accountSettings.mnemonic,
    accountSettings.email,
    accountSettings.password,
    accountSettings.pkh
  )

  const account = keys.pkh
  const request = '(Pair "' + studentAddress + '" "' + studentName + '" )'

  reportResult("Sending...", "info", "#result-bar")

  try {
    const result = await conseiljs.TezosNodeWriter.sendContractInvocationOperation(
      accountSettings.provider,
      keys,
      accountSettings.contractAddress,
      0, 100000, '', 1000, 100000,
      undefined, request,
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

$(document).ready(initUI)
