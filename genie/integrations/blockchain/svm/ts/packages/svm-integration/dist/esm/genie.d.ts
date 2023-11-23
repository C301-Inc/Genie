import * as anchor from '@coral-xyz/anchor';
import { web3 } from '@coral-xyz/anchor';
import { AnchorClient } from './utils';
export default class Genie {
    authority: web3.Keypair;
    isInitialized: boolean;
    programId: web3.PublicKey;
    client: AnchorClient;
    get key(): anchor.web3.PublicKey | undefined;
    get profileMark(): anchor.web3.PublicKey;
    get inboxMark(): anchor.web3.PublicKey;
    get program(): Promise<anchor.Program<anchor.Idl> | undefined>;
    constructor(authority: web3.Keypair, payer: web3.Keypair, programId: web3.PublicKey, endpoint: string);
    initialize(profileMarkLink?: string, inboxMarkLink?: string, webpage?: string): Promise<string>;
    private getGenieAddress;
}
//# sourceMappingURL=genie.d.ts.map