const CERTIFICATION_CONTRACT_ADDRESS = process.env.CERTIFICATION_CONTRACT_ADDRESS
  ? process.env.CERTIFICATION_CONTRACT_ADDRESS
  : null

if (CERTIFICATION_CONTRACT_ADDRESS === null) {
  throw Error('Please set CERTIFICATION_CONTRACT_ADDRESS in .env')
}

const serverInfo = {
  url: process.env.CONSEIL_API_URL,
  apiKey: process.env.CONSEIL_API_KEY,
}

function updateStatusUI(message,status, itemSelector) {
  const bar = $(itemSelector).removeClass().addClass("result-bar")

  if (status == "loading") {
    bar.addClass("result-load").html("Loading...")
  } else if (status == "True") {
    bar.addClass("result-true").html("Name: " + message)
  } else if (status == "False") {
    bar.addClass("result-false").html(message)
  } else {
    bar.addClass("result-false").html("Error: " + message)
  }
}

export function getCertStatus(inputId, outputId) {
  updateStatusUI("loading","loading", outputId)
  const contractAddress = CERTIFICATION_CONTRACT_ADDRESS

  return conseiljs.TezosConseilClient.getAccount(serverInfo, 'babylonnet', contractAddress)
    .then(account => {
      let contractStorage = account.storage.split('{')[1].split('}')[0].split('Elt')
      let students = []

      for(let i = 1; i < contractStorage.length; i++) {
        students.push([contractStorage[i].split('"')[1],contractStorage[i].split('"')[3]])
      }

      console.log(JSON.stringify(contractStorage, null, 4))
      const inputVal = $(inputId).val()

      const found = students.find(student => student[0] == inputVal)

      if(found !== undefined) {
        updateStatusUI(found[1], 'True', outputId)
      } else {
        updateStatusUI("student not found", "False", outputId)
      }
    })
    .catch(e => {
      updateStatusUI(e,e, outputId)
      console.error(e)
    })
}
