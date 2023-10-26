import Genie from './genie';
import { web3 } from '@coral-xyz/anchor';
export default class Inbox {
    genie: Genie;
    initialAuth: web3.PublicKey;
    isInitialized: boolean;
    constructor(genie: Genie, initialAuth: web3.PublicKey);
    initialize(initialAuthInboxKeypair: web3.Keypair, platform: string, primaryKey: string): Promise<string>;
    registerOwner(initialAuthInboxKeypair: web3.Keypair, initialAuthProfileKeypair: web3.Keypair): Promise<string>;
    get key(): web3.PublicKey;
    get inboxMarkAccount(): web3.PublicKey;
}
//# sourceMappingURL=inbox.d.ts.map