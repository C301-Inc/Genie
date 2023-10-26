import { Genie } from "@genie-web3/svm-integration";
import { Keypair, PublicKey } from "@solana/web3.js";

const payerKey = process.env.PAYER_KEY || "";
const GENIE_PROGRAM_ID = process.env.GENIE_PROGRAM_ID || "";
const SOLANA_ENDPOINT = process.env.SOLANA_ENDPOINT || "";

const GENIE_AUTHORITY = process.env.GENIE_AUTHORITY || "";

export const getGenie = async () => {
  const authority = Keypair.fromSecretKey(
    Uint8Array.from(JSON.parse(GENIE_AUTHORITY))
  );
  const payer = Keypair.fromSecretKey(Uint8Array.from(JSON.parse(payerKey)));

  const programId = new PublicKey(GENIE_PROGRAM_ID);
  const endpoint = SOLANA_ENDPOINT;

  const genie = new Genie(authority, payer, programId, endpoint);
  const tx = await genie.initialize();
  console.log(tx);
  return genie;
};
