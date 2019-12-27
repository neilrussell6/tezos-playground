var conseiljsCertifier =
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
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/clients/conseiljs/certification/certificate-certifier/certifier.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/clients/conseiljs/certification/certificate-certifier/certifier.js":
/*!********************************************************************************!*\
  !*** ./src/clients/conseiljs/certification/certificate-certifier/certifier.js ***!
  \********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("// This is for demonstration purposes only! Don't handle live keys like this.\n// You can hardcode your account settings and contract address here for local testing.\nfunction initUI() {\n  updateUISetting({\n    provider: \"https://rpcalpha.tzbeta.net\",\n    apiKey: \"b9labs\",\n    mnemonic: \"debris doctor pluck spatial access simple ladder network globe they august fox check much silver\",\n    password: \"QxwEIeiBfM\",\n    email: \"nfecaxpp.ixqyvcpw@tezos.example.org\",\n    contractAddress: \"KT1Noq1TJqKmecfEwBY1xxHmk5GTxEcWtRuZ\",\n  })\n  // setup all UI actions\n  $('#btn_issue').click(() => certify($('#inp_address').val(), $('#inp_name').val()))\n  $('#btn_settings').click(() => $('#settings-box').toggle())\n  $(\"#upl_input\").on(\"change\", loadJsonFile)\n  $('#btn_load').click(() => $(\"#upl_input\").click())\n}\n\nfunction updateUISetting(accountSettings) {\n  $('#provider').val(accountSettings.provider)\n  $('#apiKey').val(accountSettings.apiKey)\n  $('#mnemonic').val(accountSettings.mnemonic)\n  $('#password').val(accountSettings.password)\n  $('#email').val(accountSettings.email)\n  $('#contractAddress').val(accountSettings.contractAddress)\n}\n\nfunction readUISettings() {\n  return {\n    provider: $('#provider').val(),\n    apiKey: $('#apiKey').val(),\n    mnemonic: $('#mnemonic').val(),\n    password: $('#password').val(),\n    email: $('#email').val(),\n    contractAddress: $('#contractAddress').val()\n  }\n}\n\nfunction loadJsonFile() {\n  // This doesn't work in IE\n  const file = $(\"#upl_input\").get(0).files[0]\n  const reader = new FileReader()\n  const accountSettings = readUISettings()\n  reader.onload = parseFaucetJson(accountSettings)\n  reader.onloadend = () => updateUISetting(accountSettings)\n  reader.readAsText(file)\n}\n\n// Parses the faucet json file\nfunction parseFaucetJson(settingsToFillIn) {\n  return function (evnt) {\n    const parsed = JSON.parse(evnt.target.result)\n    settingsToFillIn.mnemonic = parsed['mnemonic'].join(\" \")\n    settingsToFillIn.password = parsed['password']\n    settingsToFillIn.email = parsed['email']\n    return settingsToFillIn\n  }\n}\n\nfunction reportResult(result, type, itemSelector) {\n  return $(itemSelector)\n    .html(result)\n    .removeClass()\n    .addClass(\"result-bar\")\n    .addClass(type == \"error\"\n              ? \"result-false\"\n              : type == \"ok\"\n                ? \"result-true\"\n                : \"result-load\")\n}\n\n// This is the main function, interacting with the contract through eztz\nasync function certify(studentAddress, studentName) {\n\n  const accountSettings = readUISettings()\n\n  const serverInfo = {\n    url: accountSettings.provider,\n    apiKey: accountSettings.apiKey,\n  }\n\n  const keys = await conseiljs.TezosWalletUtil.unlockFundraiserIdentity(\n    accountSettings.mnemonic,\n    accountSettings.email,\n    accountSettings.password,\n    accountSettings.pkh\n  )\n\n  const account = keys.pkh\n  const request = '(Pair \"' + studentAddress + '\" \"' + studentName + '\" )'\n\n  reportResult(\"Sending...\", \"info\", \"#result-bar\")\n  console.log('tezosNodeUrl', accountSettings.provider)\n  console.log('keyStore', keys)\n  console.log('toAddress', accountSettings.contractAddress)\n  console.log('amount', 0)\n  console.log('operationFee', 100000)\n  console.log('derivationPath', '')\n  console.log('storageLimit', 1000)\n  console.log('gasLimit', 100000)\n  console.log('entrypoint', undefined)\n  console.log('parameters', request)\n  console.log('parameterFormat', conseiljs.TezosParameterFormat.Michelson)\n  try {\n    const result = await conseiljs.TezosNodeWriter.sendContractInvocationOperation(\n      accountSettings.provider,\n      keys,\n      accountSettings.contractAddress,\n      0,\n      100000,\n      '',\n      1000,\n      100000,\n      undefined,\n      request,\n      conseiljs.TezosParameterFormat.Michelson,\n    )\n\n    console.table(result)\n\n    return reportResult(\n      $(\"<a>\").html(\"Op Hash: \" + result[\"operationGroupID\"]).attr(\"href\", \"https://better-call.dev/babylon/\" + result[\"operationGroupID\"].split('\"')[1]),\n      \"ok\",\n      \"#result-bar\"\n    )\n\n  } catch(e) {\n    console.log(e)\n    return reportResult(\"Error: \" + e.error, \"error\", \"#result-bar\")\n  }\n}\n\n$(document).ready(initUI)\n\n\n//# sourceURL=webpack://conseiljsCertifier/./src/clients/conseiljs/certification/certificate-certifier/certifier.js?");

/***/ })

/******/ });