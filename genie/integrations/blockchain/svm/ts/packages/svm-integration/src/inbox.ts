import Genie from './genie'
import { TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID } from './utils'
import { web3 } from '@coral-xyz/anchor'
import { getAssociatedTokenAddressSync } from '@solana/spl-token'
import Profile from './profile'
;``
export default class Inbox {
  genie: Genie
  initialAuth: web3.PublicKey
  isInitialized: boolean = false

  constructor(genie: Genie, initialAuth: web3.PublicKey) {
    this.genie = genie
    this.initialAuth = initialAuth
  }

  async initialize(
    initialAuthInboxKeypair: web3.Keypair,
    platform: string,
    primaryKey: string
  ) {
    try {
      const program = await this.genie.program

      if (program === undefined) {
        throw new Error('Genie not initialized')
      }
      if (!this.genie.isInitialized) {
        throw new Error('Genie is not initialized')
      }
      const inboxData = await program.account.inbox
        .fetch(this.key)
        .then((res) => res)
        .catch((err) => undefined)

      if (inboxData !== undefined) {
        this.isInitialized = true
        return 'already initialized'
      }

      const tx = await program.methods
        .initializeInbox(platform, primaryKey)
        .accounts({
          inbox: this.key,
          initialAuth: this.initialAuth,
          inboxMarkAccount: this.inboxMarkAccount,
          inboxMark: this.genie.inboxMark,
          genie: this.genie.key,
          payer: this.genie.client.payer.publicKey,
          tokenProgram: TOKEN_PROGRAM_ID,
          associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
          systemProgram: web3.SystemProgram.programId,
          rent: web3.SYSVAR_RENT_PUBKEY
        })
        .signers([initialAuthInboxKeypair])
        .rpc({ skipPreflight: true })
        .then((res) => res)
        .catch((error) => {
          throw new Error(error)
        })
      this.isInitialized = true
      return tx
    } catch (err) {
      throw new Error(err)
    }
  }

  async registerOwner(
    initialAuthInboxKeypair: web3.Keypair,
    initialAuthProfileKeypair: web3.Keypair
  ) {
    try {
      const program = await this.genie.program

      if (program === undefined) {
        throw new Error('Genie not initialized')
      }
      if (!this.genie.isInitialized) {
        throw new Error('Genie is not initialized')
      }

      const tx = await program.methods
        .registerInboxOwner()
        .accounts({
          payer: this.genie.client.payer.publicKey,
          inbox: this.key,
          initialAuthInbox: initialAuthInboxKeypair.publicKey,
          profile: new Profile(this.genie, initialAuthProfileKeypair.publicKey)
            .key,
          initialAuthProfile: initialAuthProfileKeypair.publicKey
        })
        .signers([initialAuthProfileKeypair, initialAuthInboxKeypair])
        .rpc({ skipPreflight: true })
        .then((res) => res)
        .catch((error) => {
          throw new Error(error)
        })
      return tx
    } catch (err) {
      throw new Error(err)
    }
  }

  get key() {
    return web3.PublicKey.findProgramAddressSync(
      [Buffer.from('inbox'), this.initialAuth.toBuffer()],
      this.genie.programId
    )[0]
  }

  get inboxMarkAccount() {
    return getAssociatedTokenAddressSync(this.genie.inboxMark, this.key, true)
  }
}
