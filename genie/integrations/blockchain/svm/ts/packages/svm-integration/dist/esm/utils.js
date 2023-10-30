import { AnchorProvider, Program, web3 } from '@coral-xyz/anchor';
import { PublicKey, Keypair, Connection, Transaction } from '@solana/web3.js';
import NodeWallet from '@coral-xyz/anchor/dist/cjs/nodewallet';
import { getAssociatedTokenAddressSync } from '@solana/spl-token';
export { TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID } from '@solana/spl-token';
import { toWeb3JsPublicKey } from '@metaplex-foundation/umi-web3js-adapters';
import { MPL_TOKEN_METADATA_PROGRAM_ID } from '@metaplex-foundation/mpl-token-metadata';
export const METADATA_PROGRAM_ID = toWeb3JsPublicKey(MPL_TOKEN_METADATA_PROGRAM_ID);
export const getErrorMessage = (error) => {
    if (error instanceof Error)
        return error.message;
    else
        return String(error);
};
export const chunk = (array, size) => {
    const chunked = [];
    let index = 0;
    while (index < array.length) {
        //@ts-ignore
        chunked.push(array.slice(index, size + index));
        index += size;
    }
    return chunked;
};
export class AnchorClient {
    constructor(payer, endpoint) {
        this.checkAccountDataIsNull = async (account) => {
            try {
                const data = await this.provider.connection.getAccountInfo(account);
                return data === null;
            }
            catch (err) {
                throw new Error(err.toString());
            }
        };
        this.getProgram = async (programIdString) => {
            let programId;
            let idl;
            try {
                programId = AnchorClient.getPublicKey(programIdString);
            }
            catch (err) {
                throw new Error(err.toString());
            }
            try {
                const data = await Program.fetchIdl(programId, this.provider);
                if (data !== null)
                    idl = data;
                else
                    throw new Error('Idl Account has no data');
            }
            catch (err) {
                throw new Error(err.toString());
            }
            const program = new Program(idl, programId, this.provider);
            return program;
        };
        this.payerSign = async (tx, signers) => {
            tx.feePayer = this.payer.publicKey;
            tx.recentBlockhash = (await this.provider.connection.getLatestBlockhash()).blockhash;
            tx = Transaction.from(tx.serialize({
                verifySignatures: false,
                requireAllSignatures: false
            }));
            tx.partialSign(this.payer);
            if (signers) {
                signers.map((v) => tx.partialSign(v));
            }
            return tx;
        };
        this.getPayerPublicKey = () => this.payer.publicKey;
        this.payer = payer;
        this.wallet = new NodeWallet(payer);
        this.endpoint = endpoint || 'http://localhost:8899';
        this.provider = new AnchorProvider(new Connection(this.endpoint, { commitment: 'confirmed' }), this.wallet, { commitment: 'confirmed' });
    }
}
AnchorClient.getPublicKey = (publicKeyString) => {
    try {
        const publicKey = new PublicKey(publicKeyString);
        return publicKey;
    }
    catch (err) {
        throw new Error('Not valid base58 encoded string');
    }
};
AnchorClient.getKeypair = (uint8ArrayString) => {
    try {
        const newKeypair = Keypair.fromSecretKey(Uint8Array.from(JSON.parse(uint8ArrayString)));
        return newKeypair;
    }
    catch (err) {
        throw new Error('Not valid uint8ArrayString');
    }
};
AnchorClient.getPublicKeys = (publicKeyStrings) => {
    const result = {};
    for (const [key, value] of Object.entries(publicKeyStrings)) {
        try {
            result[key] = new PublicKey(value);
        }
        catch (err) {
            throw new Error('Not valid base58 encoded string');
        }
    }
    return result;
};
AnchorClient.getATAAddress = (mint, owner, allowOwnerOffCurve) => {
    try {
        const ata = getAssociatedTokenAddressSync(mint, owner, allowOwnerOffCurve);
        return ata;
    }
    catch (err) {
        throw new Error(err.toString());
    }
};
export const getMetadataAddress = (mint) => {
    return web3.PublicKey.findProgramAddressSync([Buffer.from('metadata'), METADATA_PROGRAM_ID.toBuffer(), mint.toBuffer()], METADATA_PROGRAM_ID)[0];
};
//# sourceMappingURL=utils.js.map