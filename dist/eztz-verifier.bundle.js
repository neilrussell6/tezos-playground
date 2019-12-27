var eztzVerifier =
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
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/clients/eztz/certification/certificate-verifier/verifier.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/clients/eztz/certification/certificate-verifier/verifier.js":
/*!*************************************************************************!*\
  !*** ./src/clients/eztz/certification/certificate-verifier/verifier.js ***!
  \*************************************************************************/
/*! exports provided: getCertStatus */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"getCertStatus\", function() { return getCertStatus; });\nconst EZTZ_PROVIDER = \"https://rpcalpha.tzbeta.net\"\n\neztz.node.setProvider(EZTZ_PROVIDER)\n\nconst updateStatusUI = (status, itemSelector) => {\n  const bar = $(itemSelector).removeClass().addClass(\"result-bar\")\n\n  if (status == \"loading\") {\n    bar.addClass(\"result-load\").html(\"Loading...\")\n  } else if (status == \"True\") {\n    bar.addClass(\"result-true\").html(\"True\")\n  } else if (status == \"False\") {\n    bar.addClass(\"result-false\").html(\"False\")\n  } else {\n    bar.addClass(\"result-false\").html(\"Error: \" + status)\n  }\n}\n\nconst getCertStatus = (inputId, outputId) => {\n  updateStatusUI(\"loading\", outputId)\n\n  return eztz.contract.storage(\"KT1Noq1TJqKmecfEwBY1xxHmk5GTxEcWtRuZ\")\n    .then(contractStorage => {\n      console.debug(JSON.stringify(contractStorage, null, 4))\n      const students = contractStorage.args[0].map(x => x.args[0])\n      const inputVal = $(inputId).val()\n\n      const found = students.find(student => student[\"string\"] == inputVal)\n\n      if(found !== undefined) {\n        updateStatusUI(\"True\", outputId)\n      } else {\n        updateStatusUI(\"student not found\", outputId)\n      }\n    })\n    .catch(e => {\n      updateStatusUI(e, outputId)\n      console.error(e)\n    })\n}\n\n\n//# sourceURL=webpack://eztzVerifier/./src/clients/eztz/certification/certificate-verifier/verifier.js?");

/***/ })

/******/ });