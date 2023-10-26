import { TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID } from "./utils";
import { web3 } from "@coral-xyz/anchor";
import { getAssociatedTokenAddressSync } from "@solana/spl-token";
``;
export default class Profile {
    constructor(genie, initialAuth) {
        this.isInitialized = false;
        this.genie = genie;
        this.initialAuth = initialAuth;
    }
    async initialize(initialAuthProfileKeypair) {
        try {
            const program = await this.genie.program;
            if (program === undefined) {
                throw new Error("Genie not initialized");
            }
            if (!this.genie.isInitialized) {
                throw new Error("Genie is not initialized");
            }
            const profileData = await program.account.profile
                .fetch(this.key)
                .then((res) => res)
                .catch((err) => undefined);
            if (profileData !== undefined) {
                this.isInitialized = true;
                return "already initialized";
            }
            const profileMarkAccount = getAssociatedTokenAddressSync(this.genie.profileMark, this.key, true);
            const tx = await program.methods
                .initializeProfile()
                .accounts({
                profile: this.key,
                initialAuth: this.initialAuth,
                profileMarkAccount: profileMarkAccount,
                profileMark: this.genie.profileMark,
                genie: this.genie.key,
                payer: this.genie.client.payer.publicKey,
                tokenProgram: TOKEN_PROGRAM_ID,
                associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
                systemProgram: web3.SystemProgram.programId,
                rent: web3.SYSVAR_RENT_PUBKEY,
            })
                .signers([initialAuthProfileKeypair])
                .rpc({ skipPreflight: true })
                .then(res => res)
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
    get key() {
        return web3.PublicKey.findProgramAddressSync([Buffer.from("profile"), this.initialAuth.toBuffer()], this.genie.programId)[0];
    }
    get profileMarkAccount() {
        return this.genie.profileMark
            ? getAssociatedTokenAddressSync(this.genie.profileMark, this.key, true)
            : undefined;
    }
}
//# sourceMappingURL=profile.js.map