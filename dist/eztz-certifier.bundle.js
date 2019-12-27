var eztzCertifier =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/clients/eztz/certification/certificate-certifier/certifier.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/clients/eztz/certification/certificate-certifier/certifier.js":
/*!***************************************************************************!*\
  !*** ./src/clients/eztz/certification/certificate-certifier/certifier.js ***!
  \***************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("// This is for demonstration purposes only! Don't handle live keys like this.\n// You can hardcode your account settings and contract address here for local testing.\nconst EZTZ_PROVIDER = \"https://rpcalpha.tzbeta.net\"\n\neztz.node.setProvider(EZTZ_PROVIDER)\n\nfunction updateUISetting(accountSettings) {\n  $('#provider').val(accountSettings.provider)\n  $('#mnemonic').val(accountSettings.mnemonic)\n  $('#password').val(accountSettings.password)\n  $('#email').val(accountSettings.email)\n  $('#contractAddress').val(accountSettings.contractAddress)\n}\n\nfunction initUI() {\n  updateUISetting({\n    provider: EZTZ_PROVIDER,\n    contractAddress: \"KT19KZQhaYjnCdPkXN1aUcDzD1TNeXGp8JKp\",\n    mnemonic: \"debris doctor pluck spatial access simple ladder network globe they august fox check much silver\",\n    password: \"QxwEIeiBfM\",\n    email: \"nfecaxpp.ixqyvcpw@tezos.example.org\",\n  })\n\n  // setup all UI actions\n  $('#btn_issue').click(() => certify(\n    $('#inp_address').val(),\n    $('#inp_name').val(),\n  ))\n  $('#btn_settings').click(() => $('#settings-box').toggle())\n  $(\"#upl_input\").on(\"change\", loadJsonFile)\n  $('#btn_load').click(() => $(\"#upl_input\").click())\n}\n\nfunction readUISettings() {\n  return {\n    provider: $('#provider').val(),\n    mnemonic: $('#mnemonic').val(),\n    password: $('#password').val(),\n    email: $('#email').val(),\n    contractAddress: $('#contractAddress').val()\n  }\n}\n\nfunction loadJsonFile() {\n  // This doesn't work in IE\n  const file = $(\"#upl_input\").get(0).files[0]\n  const reader = new FileReader()\n  const accountSettings = readUISettings()\n  reader.onload = parseFaucetJson(accountSettings)\n  reader.onloadend = () => updateUISetting(accountSettings)\n  reader.readAsText(file)\n}\n\n// Parses the faucet json file\nfunction parseFaucetJson(settingsToFillIn) {\n  return function (evnt) {\n    const parsed = JSON.parse(evnt.target.result)\n    settingsToFillIn.mnemonic = parsed['mnemonic'].join(\" \")\n    settingsToFillIn.password = parsed['password']\n    settingsToFillIn.email = parsed['email']\n    return settingsToFillIn\n  }\n}\n\nfunction reportResult(result, type, itemSelector) {\n  return $(itemSelector)\n    .html(result)\n    .removeClass()\n    .addClass(\"result-bar\")\n    .addClass(type == \"error\"\n              ? \"result-false\"\n              : type == \"ok\"\n                ? \"result-true\"\n                : \"result-load\")\n}\n\n// This is the main function, interacting with the contract through eztz\nfunction certify(studentAddress, studentName) {\n  const accountSettings = readUISettings()\n  eztz.node.setProvider(accountSettings.provider)\n  reportResult(\"Sending...\", \"info\", \"#result-bar\")\n\n  // request\n  const keys = eztz.crypto.generateKeys(accountSettings.mnemonic, accountSettings.email + accountSettings.password)\n  const toAddress = accountSettings.contractAddress\n  const fromAddress = keys.pkh\n  const amount = 0\n  const fee = 100000\n  const gasLimit = 100000\n  const storageLimit = 1000\n  const data = `(Pair \"${studentAddress}\" \"${studentName}\")`\n\n  console.log('################################ certify : params')\n  console.log(eztz.utility.sexp2mic(data))\n\n  return eztz.rpc.sendOperation(fromAddress, {\n    kind: 'transaction',\n    fee : fee.toString(),\n    gas_limit: gasLimit.toString(),\n    amount: eztz.utility.mutez(amount).toString(),\n    destination: toAddress,\n    parameters: {\n      entrypoint: 'default',\n      value: eztz.utility.sexp2mic(data),\n    },\n    storage_limit: storageLimit.toString(),\n  }, keys)\n\n  // this hardcodes the gas limit etc for some reason:\n  // return eztz.contract.send(toAddress, fromAddress, keys, amount, data, fee)\n\n    .then(res => {\n      console.log(res)\n      reportResult(\n        $(\"<a>\").html(\"Op Hash: \" + res[\"hash\"]).attr(\"href\", \"https://better-call.dev/babylon/\" + res[\"hash\"]),\n        \"ok\",\n        \"#result-bar\")\n    })\n    .catch(e => {\n      console.log(e)\n      reportResult(\"Error: \" + e.error, \"error\", \"#result-bar\")\n    })\n}\n\n$(document).ready(initUI)\n\n\n//# sourceURL=webpack://eztzCertifier/./src/clients/eztz/certification/certificate-certifier/certifier.js?");

/***/ })

/******/ });