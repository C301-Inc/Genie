import { Genie } from "@genie-web3/svm-integration";
import {Keypair, PublicKey} from "@solana/web3.js"

const payerKey = "[165,248,47,140,124,84,119,142,207,228,192,138,41,125,68,158,138,7,92,24,92,189,105,126,92,179,188,97,55,115,48,152,244,44,73,194,233,168,27,42,232,231,221,197,97,138,223,145,170,202,31,139,100,89,191,63,123,254,56,137,48,156,33,165]"
const GENIE_PROGRAM_ID = "GENieiUYQUo8wWU2QWenWhMJuKYqwPz7u32E49t6CQLp"
const SOLANA_ENDPOINT = "https://solana-devnet-archive.allthatnode.com/Y1FYmdHjdMbGkvvZQxzUdVL5qMeCiM63"

export const getGenie = async () => {
    
    const authority = Keypair.generate();
    const payer = Keypair.fromSecretKey(Uint8Array.from(JSON.parse(payerKey)))
    const programId = new PublicKey(GENIE_PROGRAM_ID)
    const endpoint = SOLANA_ENDPOINT

    const genie = new Genie(authority, payer, programId, endpoint);
    
    
    
}