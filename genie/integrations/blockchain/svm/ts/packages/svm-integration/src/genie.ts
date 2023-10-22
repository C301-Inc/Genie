import * as anchor from "@coral-xyz/anchor";
import { web3 } from "@coral-xyz/anchor";

export default class Genie {
  authority: web3.PublicKey;
  isInitialized: boolean;

  constructor(authority: web3.PublicKey) {
    this.authority = authority;
    this.isInitialized = false;
  }
}
