// ------------------------------
// UI utils
// ------------------------------

import { KeyStore } from 'conseiljs'
import * as TezosTypes from 'conseiljs/dist/types/tezos/TezosChainTypes'

function updateUIMessage(itemSelector, status, message) {
  const bar = $(itemSelector).removeClass().addClass("result-bar")

  if (status === "loading") {
    bar.addClass("result-load").html(message)
  } else if (status === "success") {
    bar.addClass("result-true").html(message)
  } else if (status === "failure") {
    bar.addClass("result-false").html(message)
  } else if (status === "error") {
    bar.addClass("result-false").html(message)
  }
}

// ------------------------------
// logging utils
// ------------------------------

function logRequest(name, request) {
  console.log(`################################ ${name} : request`)
  Object.entries(request).forEach(([k, v]) => {
    console.log(k, v)
  })
}

function logResponse(name, response) {
  console.log(`################################ ${name} : response`)
  console.log(response)
}

function logError(name, e) {
  console.log(`################################ ${name} : error`)
  console.log(e)
}

function requestWrapper(name, request, f) {
  logRequest(name, request)
  return f(request)
    .catch((e) => {
      logError(name, e)
      return Promise.reject(e)
    })
    .then((response) => {
      logResponse(name, response)
      if (response.hasOwnProperty('results')) {
        // TODO: conseil is sometimes including the error in the operationGroupID (eg. operationGroupID: "[{"kind":"temporary","id":"failure","msg":"Error while applying operation oofdTzTuVGzNYPtr7qsn3ruUDiERenqzQpf8Ayzg9eibdgedCkN:\nbranch refused (Error:\n                  Counter 87493 already used for contract tz1bVNHSrD3sneJXQToWzzJ72eNmon2FH1D9 (expected...")
        // TODO: update this to cater for that
        const operationResults = response.results.contents.map(x => x.metadata.operation_result)
        const operationResultStatuses = operationResults.map(x => x.status)
        if (operationResultStatuses.includes('failed')) {
          const errors = operationResults.reduce((acc, x) => x.status === 'failed' ? [...acc, x.errors] : acc, [])
          logError(name, errors)
          return Promise.reject(new Error('Some operations failed'))
        }
      }
      return response
    })
}

// ------------------------------
// utils
// ------------------------------

function getKeyStore(useNonOwner = false) {
  const request = useNonOwner ? {
    contractOwnerMnemonic: process.env.CERTIFICATION_CONTRACT_NOT_OWNER_MNEMONIC,
    contractOwnerEmail: process.env.CERTIFICATION_CONTRACT_NOT_OWNER_EMAIL,
    contractOwnerPassword: process.env.CERTIFICATION_CONTRACT_NOT_OWNER_PASSWORD,
    contractOwnerPubKeyHash: process.env.CERTIFICATION_CONTRACT_NOT_OWNER_PUB_KEY_HASH,
  } : {
    contractOwnerMnemonic: process.env.CERTIFICATION_CONTRACT_OWNER_MNEMONIC,
    contractOwnerEmail: process.env.CERTIFICATION_CONTRACT_OWNER_EMAIL,
    contractOwnerPassword: process.env.CERTIFICATION_CONTRACT_OWNER_PASSWORD,
    contractOwnerPubKeyHash: process.env.CERTIFICATION_CONTRACT_OWNER_PUB_KEY_HASH,
  }
  return requestWrapper('getKeyStore', request, x => conseiljs.TezosWalletUtil.unlockFundraiserIdentity(
    x.contractOwnerMnemonic,
    x.contractOwnerEmail,
    x.contractOwnerPassword,
    x.contractOwnerPubKeyHash,
  ))
}

function sendContractPing(keyStore) {
  const contractAddress = process.env.REPEATER_CONTRACT_ADDRESS
  const request = {
    tezosNodeUrl: process.env.BABYLONNET_URL,
    keyStore,
    toAddress: contractAddress,
    operationFee: 0,
    derivationPath: '', // <-- necessary for hardware-signed operations but is unnecessary for software-signed operations
    storageLimit: 1000,
    gasLimit: 100000,
    entrypoint: undefined,
  }
  // why do we need to send entire key store to TezosNodeWriter here?
  return requestWrapper('sendContractPing', request, x => conseiljs.TezosNodeWriter.sendContractPing(
    x.tezosNodeUrl,
    x.keyStore,
    x.toAddress,
    x.operationFee,
    x.derivationPath,
    x.storageLimit,
    x.gasLimit,
    x.entrypoint,
  ))
    .then((response) => {
      return response.operationGroupID
    })
}

function sendContractInvocation(keyStore, address, name) {
  const contractAddress = process.env.CERTIFICATION_CONTRACT_ADDRESS
  const data = `(Pair "${address}" "${name}")`

  const request = {
    tezosNodeUrl: process.env.BABYLONNET_URL,
    keyStore,
    toAddress: contractAddress,
    amount: 0,
    operationFee: 100000,
    derivationPath: '', // <-- necessary for hardware-signed operations but is unnecessary for software-signed operations
    storageLimit: 1000,
    gasLimit: 100000,
    entrypoint: 'default',
    parameters: data,
    parameterFormat: conseiljs.TezosParameterFormat.Michelson,
  }
  // why do we need to send entire key store to TezosNodeWriter here?
  return requestWrapper('sendContractInvocation', request, x => conseiljs.TezosNodeWriter.sendContractInvocationOperation(
    x.tezosNodeUrl,
    x.keyStore,
    x.toAddress,
    x.amount,
    x.operationFee,
    x.derivationPath,
    x.storageLimit,
    x.gasLimit,
    x.entrypoint,
    x.parameters,
    x.parameterFormat,
  ))
    .then((response) => {
      return response.operationGroupID
    })
}

// ------------------------------
// API
// ------------------------------

// ping
// ------------------------------
// invoke contract:
//  - with no parameters
//  - with no value transfer (0 XTZ)
// does create a blockchain transaction

export function pingContract(outputId, useNonOwner = false) {
  updateUIMessage(outputId, 'loading', 'loading ...')
  return getKeyStore(useNonOwner)
    .then((keyStore) => {
      return sendContractPing(keyStore)
        .then((counter) => {
          updateUIMessage(outputId, 'success', `counter: ${counter}`)
        })
        .catch((e) => {
          updateUIMessage(outputId, 'error', e)
        })
    })
}

// invoke
// ------------------------------
// invoke contract:
//  - with parameters
//  - but no value transfer (0 XTZ)
// does create a blockchain transaction

export function invokeContract(outputId, useNonOwner = false) {
  updateUIMessage(outputId, 'loading', 'loading ...')
  const address = $('#address').val()
  const name = $('#name').val()
  return getKeyStore(useNonOwner)
    .then((keyStore) => {
      return sendContractInvocation(keyStore, address, name)
        .then((counter) => {
          updateUIMessage(outputId, 'success', `counter: ${counter}`)
        })
        .catch((e) => {
          updateUIMessage(outputId, 'error', e)
        })
    })
}
