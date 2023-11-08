import { TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID, getErrorMessage, chunk } from './utils';
import { web3 } from '@coral-xyz/anchor';
import * as anchor from '@coral-xyz/anchor';
import { getAssociatedTokenAddressSync } from '@solana/spl-token';
import { Metaplex } from '@metaplex-foundation/js';
import Profile from './profile';
export default class Inbox {
    constructor(genie, initialAuth) {
        this.isInitialized = false;
        this.genie = genie;
        this.initialAuth = initialAuth;
    }
    async initialize(initialAuthInboxKeypair, platform, primaryKey) {
        try {
            const program = await this.genie.program;
            if (program === undefined) {
                throw new Error('Genie not initialized');
            }
            if (!this.genie.isInitialized) {
                throw new Error('Genie is not initialized');
            }
            const inboxData = await program.account.inbox
                .fetch(this.key)
                .then((res) => res)
                .catch((err) => undefined);
            if (inboxData !== undefined) {
                this.isInitialized = true;
                return 'already initialized';
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
                throw new Error(error);
            });
            this.isInitialized = true;
            return tx;
        }
        catch (err) {
            throw new Error(err);
        }
    }
    async registerOwner(initialAuthInboxKeypair, initialAuthProfileKeypair) {
        try {
            const program = await this.genie.program;
            if (program === undefined) {
                throw new Error('Genie not initialized');
            }
            if (!this.genie.isInitialized) {
                throw new Error('Genie is not initialized');
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
                throw new Error(getErrorMessage(error));
            });
            return tx;
        }
        catch (err) {
            throw new Error(getErrorMessage(err));
        }
    }
    async getTokens() {
        try {
            const list = await this.genie.client.provider.connection
                .getParsedTokenAccountsByOwner(this.key, {
                programId: TOKEN_PROGRAM_ID
            })
                .then((res) => res.value
                .filter((f) => {
                return f.account.data.parsed.info.tokenAmount.decimals !== 0;
            })
                .filter((f) => f.account.data.parsed.info.tokenAmount.amount !== '0')
                .map((v) => {
                return {
                    mint: v.account.data.parsed.info.mint,
                    amount: v.account.data.parsed.info.tokenAmount.amount,
                    decimals: v.account.data.parsed.info.tokenAmount.decimals
                };
            }))
                .catch((error) => {
                throw new Error(getErrorMessage(error));
            });
            return list;
        }
        catch (err) {
            throw new Error(getErrorMessage(err));
        }
    }
    async getNfts() {
        try {
            const metaplex = new Metaplex(this.genie.client.provider.connection);
            const list = await this.genie.client.provider.connection
                .getParsedTokenAccountsByOwner(this.key, {
                programId: TOKEN_PROGRAM_ID
            })
                .then((res) => res.value
                .filter((f) => {
                return f.account.data.parsed.info.tokenAmount.decimals === 0;
            })
                .filter((f) => f.account.data.parsed.info.tokenAmount.amount !== '0')
                .map((v) => {
                return {
                    mint: v.account.data.parsed.info.mint,
                    amount: v.account.data.parsed.info.tokenAmount.amount,
                    decimals: v.account.data.parsed.info.tokenAmount.decimals
                };
            }))
                .then((res) => {
                const chunks = chunk(res, 100);
                return Promise.all(chunks.map(async (v) => {
                    const temp = await metaplex.nfts().findAllByMintList({
                        mints: v.map((k) => new web3.PublicKey(k.mint))
                    });
                    return temp;
                }));
            })
                .then((res) => {
                return res.flat();
            })
                .then((res) => {
                return res.filter((v) => v !== null);
            })
                .then((res) => {
                return Promise.all(res.map((v) => {
                    //@ts-ignore
                    return metaplex.nfts().findByMetadata({ metadata: v === null || v === void 0 ? void 0 : v.address });
                }));
            })
                .then((res) => {
                return res.map((v) => {
                    var _a, _b, _c;
                    return {
                        mint: v.mint.address.toBase58(),
                        name: (_a = v.json) === null || _a === void 0 ? void 0 : _a.name,
                        collection: (_c = (_b = v.collection) === null || _b === void 0 ? void 0 : _b.address) === null || _c === void 0 ? void 0 : _c.toBase58()
                    };
                });
            })
                .catch((error) => {
                throw new Error(getErrorMessage(error));
            });
            return list;
        }
        catch (err) {
            throw new Error(getErrorMessage(err));
        }
    }
    async sendToken(initialAuthProfileKeypair, receiverInbox, mint, amount) {
        try {
            const program = await this.genie.program;
            if (program === undefined) {
                throw new Error('Genie not initialized');
            }
            if (!this.genie.isInitialized) {
                throw new Error('Genie is not initialized');
            }
            const senderTokenAccount = getAssociatedTokenAddressSync(mint, this.key, true);
            const receiverInboxTokenAccount = getAssociatedTokenAddressSync(mint, receiverInbox, true);
            const tx = await program.methods
                .sendToken(new anchor.BN(amount))
                .accounts({
                payer: this.genie.client.payer.publicKey,
                mint: mint,
                senderProfileAuth: initialAuthProfileKeypair.publicKey,
                senderProfile: new Profile(this.genie, initialAuthProfileKeypair.publicKey).key,
                senderInbox: this.key,
                senderTokenAccount: senderTokenAccount,
                receiverInbox,
                receiverTokenAccount: receiverInboxTokenAccount,
                tokenProgram: TOKEN_PROGRAM_ID,
                associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
                systemProgram: web3.SystemProgram.programId,
                rent: web3.SYSVAR_RENT_PUBKEY
            })
                .signers([initialAuthProfileKeypair])
                .rpc({ skipPreflight: true })
                .then((res) => res)
                .catch((error) => {
                throw new Error(getErrorMessage(error));
            });
            return tx;
        }
        catch (err) {
            throw new Error(getErrorMessage(err));
        }
    }
    get key() {
        return web3.PublicKey.findProgramAddressSync([Buffer.from('inbox'), this.initialAuth.toBuffer()], this.genie.programId)[0];
    }
    get inboxMarkAccount() {
        return getAssociatedTokenAddressSync(this.genie.inboxMark, this.key, true);
    }
}
//# sourceMappingURL=inbox.js.map