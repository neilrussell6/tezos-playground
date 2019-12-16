const EZTZ_PROVIDER = process.env.EZTZ_PROVIDER ? process.env.EZTZ_PROVIDER : 'http://localhost:8732'
const EZTZ_CONTRACT_ADDRESS = process.env.EZTZ_CONTRACT_ADDRESS ? process.env.EZTZ_CONTRACT_ADDRESS : null

if (EZTZ_CONTRACT_ADDRESS === null) {
  throw Error('Please set EZTZ_CONTRACT_ADDRESS in .env.local')
}

eztz.node.setProvider(EZTZ_PROVIDER)

const updateStatusUI = (status, itemSelector) => {
  const bar = $(itemSelector).removeClass().addClass("result-bar")

  if (status == "loading") {
    bar.addClass("result-load").html("Loading...")
  } else if (status == "True") {
    bar.addClass("result-true").html("True")
  } else if (status == "False") {
    bar.addClass("result-false").html("False")
  } else {
    bar.addClass("result-false").html("Error: " + status)
  }
}

export const getCertStatus = ({ EZTZ_CONTRACT_ADDRESS }) => (inputId, outputId) => {
  updateStatusUI("loading", outputId)

  return eztz.contract.storage(EZTZ_CONTRACT_ADDRESS)
    .then(contractStorage => {
      console.debug(JSON.stringify(contractStorage, null, 4))
      const students = contractStorage.args[0].map(x => x.args[0])
      const inputVal = $(inputId).val()

      const found = students.find(student => student["string"] == inputVal)

      if(found !== undefined) {
        updateStatusUI("True", outputId)
      } else {
        updateStatusUI("student not found", outputId)
      }
    })
    .catch(e => {
      updateStatusUI(e, outputId)
      console.error(e)
    })
}
