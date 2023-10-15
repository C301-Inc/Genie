import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { Genie } from "../target/types/genie";
import { web3 } from "@coral-xyz/anchor";
import { toWeb3JsPublicKey } from "@metaplex-foundation/umi-web3js-adapters";
import { MPL_TOKEN_METADATA_PROGRAM_ID } from "@metaplex-foundation/mpl-token-metadata";

anchor.setProvider(anchor.AnchorProvider.env());

const program = anchor.workspace.Genie as Program<Genie>;
const METADATA_PROGRAM_ID = toWeb3JsPublicKey(MPL_TOKEN_METADATA_PROGRAM_ID);

export const getProfileAddress = (initialAuth: web3.PublicKey) => {
  return web3.PublicKey.findProgramAddressSync(
    [Buffer.from("profile"), initialAuth.toBuffer()],
    program.programId
  )[0];
};

export const getInboxAddress = (initialAuth: web3.PublicKey) => {
  return web3.PublicKey.findProgramAddressSync(
    [Buffer.from("inbox"), initialAuth.toBuffer()],
    program.programId
  )[0];
};

export const getGenieAddress = (authority: web3.PublicKey) => {
  return web3.PublicKey.findProgramAddressSync(
    [Buffer.from("genie"), authority.toBuffer()],
    program.programId
  )[0];
};

export const getProfileMarkAddress = (genie: web3.PublicKey) => {
  return web3.PublicKey.findProgramAddressSync(
    [Buffer.from("genie_profile"), genie.toBuffer()],
    program.programId
  )[0];
};

export const getInboxMarkAddress = (genie: web3.PublicKey) => {
  return web3.PublicKey.findProgramAddressSync(
    [Buffer.from("genie_inbox"), genie.toBuffer()],
    program.programId
  )[0];
};

export const getMetadataAddress = (mint: web3.PublicKey) => {
  return web3.PublicKey.findProgramAddressSync(
    [Buffer.from("metadata"), METADATA_PROGRAM_ID.toBuffer(), mint.toBuffer()],
    METADATA_PROGRAM_ID
  )[0];
};
