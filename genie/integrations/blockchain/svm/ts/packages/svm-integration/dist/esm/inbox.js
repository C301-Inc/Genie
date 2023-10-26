import { TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID } from "./utils";
import { web3 } from "@coral-xyz/anchor";
import { getAssociatedTokenAddressSync } from "@solana/spl-token";
``;
export default class Inbox {
    constructor(genie, initialAuth) {
        this.isInitialized = false;
        this.genie = genie;
        this.initialAuth = initialAuth;
    }
    async initialize(initialAuthInboxKeypair) {
        try {
            const program = await this.genie.program;
            if (program === undefined) {
                throw new Error("Genie not initialized");
            }
            if (this.genie.inboxMark === undefined) {
                throw new Error("Genie inboxMark not initialized");
            }
            const inboxData = await program.account.inbox
                .fetch(this.key)
                .then((res) => res)
                .catch((err) => undefined);
            if (inboxData !== undefined) {
                this.isInitialized = true;
                return "already initialized";
            }
            const tx = await program.methods
                .initializeInbox()
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
                rent: web3.SYSVAR_RENT_PUBKEY,
            })
                .signers([initialAuthInboxKeypair])
                .rpc({ skipPreflight: true })
                .then((res) => res)
                .catch((error) => {
                throw new Error("inbox initialization failed");
            });
            this.isInitialized = true;
            return tx;
        }
        catch (err) { }
    }
    get key() {
        return web3.PublicKey.findProgramAddressSync([Buffer.from("inbox"), this.initialAuth.toBuffer()], this.genie.programId)[0];
    }
    get inboxMarkAccount() {
        return this.genie.inboxMark
            ? getAssociatedTokenAddressSync(this.genie.inboxMark, this.key, true)
            : undefined;
    }
}
//# sourceMappingURL=inbox.js.map