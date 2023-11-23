import { web3 } from '@coral-xyz/anchor';
import { AnchorClient, getErrorMessage, getMetadataAddress, METADATA_PROGRAM_ID, TOKEN_PROGRAM_ID } from './utils';
export default class Genie {
    get key() {
        return this.getGenieAddress(this.authority.publicKey);
    }
    get profileMark() {
        return web3.PublicKey.findProgramAddressSync([Buffer.from('genie_profile'), this.key.toBuffer()], this.programId)[0];
    }
    get inboxMark() {
        return web3.PublicKey.findProgramAddressSync([Buffer.from('genie_inbox'), this.key.toBuffer()], this.programId)[0];
    }
    get program() {
        return (async () => {
            const program = await this.client
                .getProgram(this.programId.toBase58())
                .catch(() => undefined);
            return program;
        })();
    }
    constructor(authority, payer, programId, endpoint) {
        this.isInitialized = false;
        this.authority = authority;
        this.programId = programId;
        this.client = new AnchorClient(payer, endpoint);
    }
    async initialize(profileMarkLink = 'https://arweave.net/5XNlZK1agbCZgdJS50TwEl9SG-mhz-rndidoFi37Hzc', inboxMarkLink = 'https://arweave.net/JbzEfZANGNoLIzP35Yj7ziFWKUrkQWhstehjS8l3OjU', webpage = 'https://www.geniebridge.link') {
        try {
            const program = await this.program;
            if (program === undefined) {
                throw new Error('Program not initialized');
            }
            const genieData = await program.account.genie
                .fetch(this.key)
                .then((res) => res)
                .catch((err) => undefined);
            if (genieData !== undefined) {
                this.isInitialized = true;
                return 'already initialized';
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
                rent: web3.SYSVAR_RENT_PUBKEY
            })
                .signers([this.authority])
                .rpc({ skipPreflight: true })
                .then((res) => res)
                .catch((error) => {
                throw new Error('genie initialization failed');
            });
            this.isInitialized = true;
            return tx;
        }
        catch (err) {
            throw new Error(getErrorMessage(err));
        }
    }
    getGenieAddress(authority) {
        return this.programId
            ? web3.PublicKey.findProgramAddressSync([Buffer.from('genie'), authority.toBuffer()], this.programId)[0]
            : undefined;
    }
}
//# sourceMappingURL=genie.js.map