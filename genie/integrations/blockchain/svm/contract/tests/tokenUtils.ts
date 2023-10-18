import { AnchorProvider, web3 } from "@coral-xyz/anchor";
import { associatedAddress } from "@coral-xyz/anchor/dist/cjs/utils/token";
import {
  createInitializeMintInstruction,
  createInitializeAccount3Instruction,
  createMintToInstruction,
  createAssociatedTokenAccountInstruction,
  getAccount,
} from "@solana/spl-token";

class TestToken {
  tokenMintKeypair: web3.Keypair;
  tokenMint: web3.PublicKey;
  decimal: number;
  provider: AnchorProvider;
  isInitialized: boolean = false;
  payer: web3.PublicKey;
  connection: web3.Connection;

  constructor(decimal: number, provider: AnchorProvider) {
    this.tokenMintKeypair = web3.Keypair.generate();
    this.tokenMint = this.tokenMintKeypair.publicKey;
    this.decimal = decimal;
    this.provider = provider;
    this.payer = provider.wallet.publicKey;
    this.connection = provider.connection;
  }

  async mintToken(amount: number, receiver: web3.PublicKey) {
    let tx: web3.Transaction;
    let signers: web3.Keypair[] = [];
    const receiverAta = associatedAddress({
      mint: this.tokenMint,
      owner: receiver,
    });
    if (!this.isInitialized) {
      tx.add(
        createInitializeMintInstruction(
          this.tokenMint,
          this.decimal,
          this.payer,
          this.payer
        )
      );
      signers.push(this.tokenMintKeypair);
    }

    const ataInitialized: boolean = await getAccount(
      this.provider.connection,
      receiverAta
    )
      .then((res) => true)
      .catch((err) => false);

    if (!ataInitialized) {
      tx.add(
        createAssociatedTokenAccountInstruction(
          this.payer,
          receiverAta,
          receiver,
          this.tokenMint
        )
      );
    }

    tx.add(
      createMintToInstruction(this.tokenMint, receiverAta, this.payer, amount)
    );

    const result = this.provider
      .sendAndConfirm(tx, signers, { skipPreflight: true })
      .then((res) => {
        return { txId: res, success: true };
      })
      .catch((err) => {
        return { txid: "", success: false };
      });
    return result;
  }
}
