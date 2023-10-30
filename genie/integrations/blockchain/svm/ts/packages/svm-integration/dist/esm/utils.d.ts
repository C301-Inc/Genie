import { AnchorProvider, Program, web3 } from '@coral-xyz/anchor';
import { PublicKey, Keypair, Transaction } from '@solana/web3.js';
import NodeWallet from '@coral-xyz/anchor/dist/cjs/nodewallet';
export { TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID } from '@solana/spl-token';
export declare const METADATA_PROGRAM_ID: web3.PublicKey;
export declare const getErrorMessage: (error: unknown) => string;
export declare const chunk: (array: any[], size: number) => any[];
export declare class AnchorClient {
    provider: AnchorProvider;
    payer: Keypair;
    wallet: NodeWallet;
    endpoint: string;
    constructor(payer: web3.Keypair, endpoint?: string);
    static getPublicKey: (publicKeyString: string) => PublicKey;
    static getKeypair: (uint8ArrayString: string) => Keypair;
    static getPublicKeys: (publicKeyStrings: {
        [key: string]: string;
    }) => {
        [key: string]: web3.PublicKey;
    };
    static getATAAddress: (mint: PublicKey, owner: PublicKey, allowOwnerOffCurve?: boolean) => PublicKey;
    checkAccountDataIsNull: (account: PublicKey) => Promise<boolean>;
    getProgram: (programIdString: string) => Promise<Program>;
    payerSign: (tx: Transaction, signers?: Keypair[]) => Promise<web3.Transaction>;
    getPayerPublicKey: () => web3.PublicKey;
}
export declare const getMetadataAddress: (mint: web3.PublicKey) => web3.PublicKey;
//# sourceMappingURL=utils.d.ts.map