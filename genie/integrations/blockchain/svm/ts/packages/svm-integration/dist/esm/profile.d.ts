import Genie from "./genie";
import { web3 } from "@coral-xyz/anchor";
export default class Profile {
    genie: Genie;
    initialAuth: web3.PublicKey;
    isInitialized: boolean;
    constructor(genie: Genie, initialAuth: web3.PublicKey);
    initialize(initialAuthProfileKeypair: web3.Keypair): Promise<string>;
    get key(): web3.PublicKey;
    get profileMarkAccount(): web3.PublicKey | undefined;
}
//# sourceMappingURL=profile.d.ts.map