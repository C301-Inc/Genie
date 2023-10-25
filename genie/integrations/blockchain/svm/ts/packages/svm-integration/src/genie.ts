import * as anchor from "@coral-xyz/anchor";
import { web3, Program } from "@coral-xyz/anchor";
import {
  AnchorClient,
  getMetadataAddress,
  METADATA_PROGRAM_ID,
  TOKEN_PROGRAM_ID,
} from "./utils";

export default class Genie {
  authority: web3.Keypair;
  isInitialized: boolean = false;
  programId: web3.PublicKey;
  client: AnchorClient;

  get key() {
    return this.isInitialized
      ? this.getGenieAddress(this.authority.publicKey)
      : undefined;
  }

  get profileMark() {
    return this.key
      ? web3.PublicKey.findProgramAddressSync(
          [Buffer.from("genie_profile"), this.key.toBuffer()],
          this.programId
        )[0]
      : undefined;
  }

  get inboxMark() {
    return this.key
      ? web3.PublicKey.findProgramAddressSync(
          [Buffer.from("genie_inbox"), this.key.toBuffer()],
          this.programId
        )[0]
      : undefined;
  }

  get program() {
    return (async () => {
      const program = await this.client
        .getProgram(this.programId.toBase58())
        .catch(() => undefined);
      return program;
    })();
  }

  constructor(
    authority: web3.Keypair,
    payer: web3.Keypair,
    programId: web3.PublicKey,
    endpoint: string
  ) {
    this.authority = authority;
    this.programId = programId;
    const client = new AnchorClient(payer.secretKey.toString(), endpoint);
  }

  async initialize(
    profileMarkLink: string = "https://arweave.net/5XNlZK1agbCZgdJS50TwEl9SG-mhz-rndidoFi37Hzc",
    inboxMarkLink: string = "https://arweave.net/JbzEfZANGNoLIzP35Yj7ziFWKUrkQWhstehjS8l3OjU",
    webpage: string = "https://www.geniebridge.link"
  ) {
    try {
      const program = await this.program;

      if (program === undefined) {
        throw new Error("Program not initialized");
      }
      if (
        this.key === undefined ||
        this.profileMark === undefined ||
        this.inboxMark === undefined
      ) {
        throw new Error("genie not setted");
      }

      const genieData = await program.account.genie
        .fetch(this.key)
        .then((res) => res)
        .catch((err) => undefined);

      if (genieData !== undefined) {
        this.isInitialized = true;
        return this.key;
      }

      const tx = await program.methods
        .initializeGenie(profileMarkLink, inboxMarkLink, webpage)
        .accounts({
          genie: this.key,
          profileMark: this.profileMark,
          profileMetadata: getMetadataAddress(this.profileMark),
          inboxMark: this.inboxMark,
          inboxMetadata: getMetadataAddress(this.inboxMark),
          authority: this.authority.publicKey,
          payer: this.client.payer.publicKey,
          systemProgram: web3.SystemProgram.programId,
          tokenProgram: TOKEN_PROGRAM_ID,
          metadataProgram: METADATA_PROGRAM_ID,
          rent: web3.SYSVAR_RENT_PUBKEY,
        })
        .signers([this.authority])
        .rpc({ skipPreflight: true })
        .then((res) => res)
        .catch((error) => {
          throw new Error("genie initialization failed");
        });
      this.isInitialized = true;
      return this.key;
    } catch (err) {
      throw new Error(err);
    }
  }

  private getGenieAddress(authority: web3.PublicKey) {
    return this.programId
      ? web3.PublicKey.findProgramAddressSync(
          [Buffer.from("genie"), authority.toBuffer()],
          this.programId
        )[0]
      : undefined;
  }
}
