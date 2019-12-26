// This is for demonstration purposes only! Don't handle live keys like this.
// You can hardcode your account settings and contract address here for local testing.
const EZTZ_PROVIDER = process.env.BABYLONNET_URL

eztz.node.setProvider(EZTZ_PROVIDER)

function updateUISetting(accountSettings) {
  $('#provider').val(accountSettings.provider);
  $('#mnemonic').val(accountSettings.mnemonic);
  $('#password').val(accountSettings.password);
  $('#email').val(accountSettings.email);
  $('#contractAddress').val(accountSettings.contractAddress);
}

function initUI() {
  updateUISetting({
    provider: EZTZ_PROVIDER,
    contractAddress: process.env.CERTIFICATION_CONTRACT_ADDRESS,
    mnemonic: process.env.CERTIFICATION_CONTRACT_OWNER_MNEMONIC,
    password: process.env.CERTIFICATION_CONTRACT_OWNER_PASSWORD,
    email: process.env.CERTIFICATION_CONTRACT_OWNER_EMAIL,
  });

  // setup all UI actions
  $('#btn_issue').click(() => certify($('#inp_address').val()));
  $('#btn_settings').click(() => $('#settings-box').toggle());
  $("#upl_input").on("change", loadJsonFile);
  $('#btn_load').click(() => $("#upl_input").click());
}

function readUISettings() {
  return {
    provider: $('#provider').val(),
    mnemonic: $('#mnemonic').val(),
    password: $('#password').val(),
    email: $('#email').val(),
    contractAddress: $('#contractAddress').val()
  };
}

function loadJsonFile() {
  // This doesn't work in IE
  const file = $("#upl_input").get(0).files[0];
  const reader = new FileReader();
  const accountSettings = readUISettings();
  reader.onload = parseFaucetJson(accountSettings);
  reader.onloadend = () => updateUISetting(accountSettings);
  reader.readAsText(file);
}

// Parses the faucet json file
function parseFaucetJson(settingsToFillIn) {
  return function (evnt) {
    const parsed = JSON.parse(evnt.target.result);
    settingsToFillIn.mnemonic = parsed['mnemonic'].join(" ");
    settingsToFillIn.password = parsed['password'];
    settingsToFillIn.email = parsed['email'];
    return settingsToFillIn;
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
                : "result-load");
}

// This is the main function, interacting with the contract through eztz
function certify(studentAddress) {
  const accountSettings = readUISettings();

  eztz.node.setProvider(accountSettings.provider);
  const keys = eztz.crypto.generateKeys(accountSettings.mnemonic, accountSettings.email + accountSettings.password);
  const account = keys.pkh;
  const request = '"' + studentAddress + '"';

  reportResult("Sending...", "info", "#result-bar");

  const _request = `(Pair "${request}" "Student 2")`
  return eztz.contract.send(accountSettings.contractAddress, account, keys, 0, request, "0100000", 100000, 60000)
    .then(res => {
      reportResult(
        $("<a>").html("Op Hash: " + res["hash"]).attr("href", "https://better-call.dev/babylon/" + res["hash"]),
        "ok",
        "#result-bar")
    })
    .catch(e => {
      console.log(e);
      reportResult("Error: " + e.error, "error", "#result-bar");
    });
}

$(document).ready(initUI);
