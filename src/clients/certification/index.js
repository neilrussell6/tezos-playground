import { getCertStatus as _getCertStatus } from './certificate-verifier/verifier'

const EZTZ_PROVIDER = process.env.EZTZ_PROVIDER ? process.env.EZTZ_PROVIDER : 'http://localhost:8732'
const EZTZ_CONTRACT_ADDRESS = process.env.EZTZ_CONTRACT_ADDRESS ? process.env.EZTZ_CONTRACT_ADDRESS : null

if (EZTZ_CONTRACT_ADDRESS === null) {
  throw Error('Please set EZTZ_CONTRACT_ADDRESS in .env.local')
}

eztz.node.setProvider(EZTZ_PROVIDER)

export const getCertStatus = _getCertStatus({ EZTZ_CONTRACT_ADDRESS })
