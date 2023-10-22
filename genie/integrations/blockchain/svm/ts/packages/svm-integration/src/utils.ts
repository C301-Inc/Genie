import { AnchorProvider, Program, Idl, web3 } from "@coral-xyz/anchor";
import { PublicKey, Keypair, Connection, Transaction } from "@solana/web3.js";
import NodeWallet from "@coral-xyz/anchor/dist/cjs/nodewallet";
import { getAssociatedTokenAddressSync } from "@solana/spl-token";
export { TOKEN_PROGRAM_ID } from "@solana/spl-token";

import { toWeb3JsPublicKey } from "@metaplex-foundation/umi-web3js-adapters";
import { MPL_TOKEN_METADATA_PROGRAM_ID } from "@metaplex-foundation/mpl-token-metadata";

export const METADATA_PROGRAM_ID = toWeb3JsPublicKey(
  MPL_TOKEN_METADATA_PROGRAM_ID
);

export class AnchorClient {
  provider: AnchorProvider;
  payer: Keypair;
  wallet: NodeWallet;
  endpoint: string;

  constructor(payerUint8ArrayString: string, endpoint?: string) {
    const payer = AnchorClient.getKeypair(payerUint8ArrayString);
    this.payer = payer;
    this.wallet = new NodeWallet(payer);
    this.endpoint = endpoint || "http://localhost:8899";
    this.provider = new AnchorProvider(
      new Connection(this.endpoint, { commitment: "confirmed" }),
      this.wallet,
      { commitment: "confirmed" }
    );
  }

  static getPublicKey = (publicKeyString: string): PublicKey => {
    try {
      const publicKey = new PublicKey(publicKeyString);
      return publicKey;
    } catch (err) {
      throw new Error("Not valid base58 encoded string");
    }
  };

  static getKeypair = (uint8ArrayString: string): Keypair => {
    try {
      const newKeypair = Keypair.fromSecretKey(
        Uint8Array.from(JSON.parse(uint8ArrayString))
      );
      return newKeypair;
    } catch (err) {
      throw new Error("Not valid uint8ArrayString");
    }
  };

  static getPublicKeys = (publicKeyStrings: {
    [key: string]: string;
  }): { [key: string]: PublicKey } => {
    const result = {};
    for (const [key, value] of Object.entries(publicKeyStrings)) {
      try {
        result[key] = new PublicKey(value);
      } catch (err) {
        throw new Error("Not valid base58 encoded string");
      }
    }
    return result;
  };

  static getATAAddress = (
    mint: PublicKey,
    owner: PublicKey,
    allowOwnerOffCurve?: boolean
  ): PublicKey => {
    try {
      const ata = getAssociatedTokenAddressSync(
        mint,
        owner,
        allowOwnerOffCurve
      );
      return ata;
    } catch (err) {
      throw new Error(err.toString());
    }
  };

  checkAccountDataIsNull = async (account: PublicKey): Promise<boolean> => {
    try {
      const data = await this.provider.connection.getAccountInfo(account);
      return data === null;
    } catch (err) {
      throw new Error(err.toString());
    }
  };

  getProgram = async (programIdString: string): Promise<Program> => {
    let programId: PublicKey;
    let idl: Idl;

    try {
      programId = AnchorClient.getPublicKey(programIdString);
    } catch (err) {
      throw new Error(err.toString());
    }

    try {
      const data = await Program.fetchIdl(programId, this.provider);
      if (data !== null) idl = data;
      else throw new ErrorEvent("Idl Account has no data");
    } catch (err) {
      throw new Error(err.toString());
    }

    const program = new Program(idl!, programId, this.provider);

    return program;
  };

  payerSign = async (tx: Transaction, signers?: Keypair[]) => {
    tx.feePayer = this.payer.publicKey;
    tx.recentBlockhash = (
      await this.provider.connection.getLatestBlockhash()
    ).blockhash;
    tx = Transaction.from(
      tx.serialize({
        verifySignatures: false,
        requireAllSignatures: false,
      })
    );
    tx.partialSign(this.payer);
    if (signers) {
      signers.map((v) => tx.partialSign(v));
    }
    return tx;
  };

  getPayerPublicKey = () => this.payer.publicKey;
}

export const getMetadataAddress = (mint: web3.PublicKey) => {
  return web3.PublicKey.findProgramAddressSync(
    [Buffer.from("metadata"), METADATA_PROGRAM_ID.toBuffer(), mint.toBuffer()],
    METADATA_PROGRAM_ID
  )[0];
};
