import Genie from './genie'
import {
  TOKEN_PROGRAM_ID,
  ASSOCIATED_TOKEN_PROGRAM_ID,
  getErrorMessage,
  chunk
} from './utils'
import { web3 } from '@coral-xyz/anchor'
import { getAssociatedTokenAddressSync } from '@solana/spl-token'
import { Metaplex } from '@metaplex-foundation/js'
import Profile from './profile'
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
          throw new Error(getErrorMessage(error))
        })
      return tx
    } catch (err) {
      throw new Error(getErrorMessage(err))
    }
  }
  async getTokens() {
    try {
      const list = await this.genie.client.provider.connection
        .getParsedTokenAccountsByOwner(this.key, {
          programId: TOKEN_PROGRAM_ID
        })
        .then((res) =>
          res.value
            .filter((f) => {
              return f.account.data.parsed.info.tokenAmount.decimals !== 0
            })
            .filter(
              (f) => f.account.data.parsed.info.tokenAmount.amount !== '0'
            )
            .map((v) => {
              return {
                mint: v.account.data.parsed.info.mint,
                amount: v.account.data.parsed.info.tokenAmount.amount,
                decimals: v.account.data.parsed.info.tokenAmount.decimals
              }
            })
        )
        .catch((error) => {
          throw new Error(getErrorMessage(error))
        })
      const solanaBalance = await this.genie.client.provider.connection
        .getBalance(this.key)
        .then((res) => res - 3549600)
      list.splice(0, 0, {
        mint: 'native sol',
        amount: solanaBalance.toString(),
        decimals: 9
      })
      return list
    } catch (err) {
      throw new Error(getErrorMessage(err))
    }
  }

  async getNfts() {
    try {
      const metaplex = new Metaplex(this.genie.client.provider.connection)
      const list = await this.genie.client.provider.connection
        .getParsedTokenAccountsByOwner(this.key, {
          programId: TOKEN_PROGRAM_ID
        })
        .then((res) =>
          res.value
            .filter((f) => {
              return f.account.data.parsed.info.tokenAmount.decimals === 0
            })
            .filter(
              (f) => f.account.data.parsed.info.tokenAmount.amount !== '0'
            )
            .map((v) => {
              return {
                mint: v.account.data.parsed.info.mint,
                amount: v.account.data.parsed.info.tokenAmount.amount,
                decimals: v.account.data.parsed.info.tokenAmount.decimals
              }
            })
        )
        .then((res) => {
          const chunks = chunk(res, 100)

          return Promise.all(
            chunks.map(async (v) => {
              const temp = await metaplex.nfts().findAllByMintList({
                mints: v.map((k) => new web3.PublicKey(k.mint))
              })
              return temp
            })
          )
        })
        .then((res) => {
          return res.flat()
        })
        .then((res) => {
          return res.filter((v) => v !== null)
        })
        .then((res) => {
          return Promise.all(
            res.map((v) => {
              //@ts-ignore
              return metaplex.nfts().findByMetadata({ metadata: v?.address })
            })
          )
        })
        .then((res) => {
          return res.map((v) => {
            return {
              mint: v.mint.address.toBase58(),
              name: v.json?.name,
              collection: v.collection?.address?.toBase58()
            }
          })
        })
        .catch((error) => {
          throw new Error(getErrorMessage(error))
        })
      return list
    } catch (err) {
      throw new Error(getErrorMessage(err))
    }
  }

  async sendToken(
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
          throw new Error(getErrorMessage(error))
        })
      return tx
    } catch (err) {
      throw new Error(getErrorMessage(err))
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
