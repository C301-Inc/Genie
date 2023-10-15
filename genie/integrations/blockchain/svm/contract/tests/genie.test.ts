import * as anchor from "@coral-xyz/anchor";
import { BN, Program } from "@coral-xyz/anchor";
import { Genie } from "../target/types/genie";
import { web3 } from "@coral-xyz/anchor";
import {
  ASSOCIATED_PROGRAM_ID,
  TOKEN_PROGRAM_ID,
} from "@coral-xyz/anchor/dist/cjs/utils/token";
import { MPL_TOKEN_METADATA_PROGRAM_ID } from "@metaplex-foundation/mpl-token-metadata";
import { toWeb3JsPublicKey } from "@metaplex-foundation/umi-web3js-adapters";
import { getAssociatedTokenAddressSync } from "@solana/spl-token";
import {
  createInitializeMintInstruction,
  createAssociatedTokenAccountInstruction,
  createMintToCheckedInstruction,
  getMinimumBalanceForRentExemptMint,
  MINT_SIZE,
} from "@solana/spl-token";
import {
  getGenieAddress,
  getInboxAddress,
  getInboxMarkAddress,
  getMetadataAddress,
  getProfileAddress,
  getProfileMarkAddress,
} from "./utils";

describe("genie", () => {
  // Configure the client to use the local cluster.
  anchor.setProvider(anchor.AnchorProvider.env());

  const program = anchor.workspace.Genie as Program<Genie>;
  const METADATA_PROGRAM_ID = toWeb3JsPublicKey(MPL_TOKEN_METADATA_PROGRAM_ID);

  const genieAuthKeypair = web3.Keypair.generate();
  const genieAuth = genieAuthKeypair.publicKey;

  const genie = getGenieAddress(genieAuth);

  const profileMark = getProfileMarkAddress(genie);

  const profileMetadata = getMetadataAddress(profileMark);

  const inboxMark = getInboxMarkAddress(genie);

  const inboxMetadata = getMetadataAddress(inboxMark);

  const initialAuthProfileKeypair = web3.Keypair.generate();
  const initialAuthProfile = initialAuthProfileKeypair.publicKey;

  const profile = getProfileAddress(initialAuthProfile);
  const profileMarkAccount = getAssociatedTokenAddressSync(
    profileMark,
    profile,
    true
  );

  const initialAuthInboxKeypair = web3.Keypair.generate();
  const initialAuthInbox = initialAuthInboxKeypair.publicKey;

  const inbox = getInboxAddress(initialAuthInbox);
  const inboxMarkAccount = getAssociatedTokenAddressSync(
    inboxMark,
    inbox,
    true
  );

  const newAuthKeypair = web3.Keypair.generate();
  const newAuth = newAuthKeypair.publicKey;

  const newAuth2Keypair = web3.Keypair.generate();
  const newAuth2 = newAuth2Keypair.publicKey;

  const payer = anchor.AnchorProvider.env().wallet.publicKey;

  it("genie initialized!", async () => {
    // Add your test here.
    const tx = await program.methods
      .initializeGenie(
        "https://arweave.net/5XNlZK1agbCZgdJS50TwEl9SG-mhz-rndidoFi37Hzc",
        "https://arweave.net/JbzEfZANGNoLIzP35Yj7ziFWKUrkQWhstehjS8l3OjU",
        "https://www.geniebridge.link"
      )
      .accounts({
        genie,
        profileMark,
        profileMetadata,
        inboxMark,
        inboxMetadata,
        authority: genieAuth,
        payer,
        systemProgram: web3.SystemProgram.programId,
        tokenProgram: TOKEN_PROGRAM_ID,
        metadataProgram: METADATA_PROGRAM_ID,
        rent: web3.SYSVAR_RENT_PUBKEY,
      })
      .signers([genieAuthKeypair])
      .rpc({ skipPreflight: true })
      .then((res) => res)
      .catch((error) => {
        console.log(error);
      });

    console.log({
      genie: genie.toString(),
      profileMark: profileMark.toString(),
      inboxMark: inboxMark.toString(),
    });
    console.log("Your transaction signature", tx);
  });

  it("profile initialized!", async () => {
    console.log({
      initialAuthPublicKey: initialAuthProfileKeypair.publicKey.toBase58(),
      initialAuthSecretKey: initialAuthProfileKeypair.secretKey.toString(),
    });

    // Add your test here.
    const tx = await program.methods
      .initializeProfile()
      .accounts({
        profile,
        initialAuth: initialAuthProfile,
        profileMarkAccount,
        profileMark,
        genie,
        payer,
        tokenProgram: TOKEN_PROGRAM_ID,
        associatedTokenProgram: ASSOCIATED_PROGRAM_ID,
        systemProgram: web3.SystemProgram.programId,
        rent: web3.SYSVAR_RENT_PUBKEY,
      })
      .signers([initialAuthProfileKeypair])
      .rpc({ skipPreflight: true })
      .then((res) => res)
      .catch((error) => {
        console.log(error);
      });
    console.log("Your transaction signature", tx);
  });
});
