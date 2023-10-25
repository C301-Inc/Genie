var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
import { AnchorProvider, Program, web3 } from "@coral-xyz/anchor";
import { PublicKey, Keypair, Connection, Transaction } from "@solana/web3.js";
import NodeWallet from "@coral-xyz/anchor/dist/cjs/nodewallet";
import { getAssociatedTokenAddressSync } from "@solana/spl-token";
export { TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID, } from "@solana/spl-token";
import { toWeb3JsPublicKey } from "@metaplex-foundation/umi-web3js-adapters";
import { MPL_TOKEN_METADATA_PROGRAM_ID } from "@metaplex-foundation/mpl-token-metadata";
export var METADATA_PROGRAM_ID = toWeb3JsPublicKey(MPL_TOKEN_METADATA_PROGRAM_ID);
var AnchorClient = /** @class */ (function () {
    function AnchorClient(payerUint8ArrayString, endpoint) {
        var _this = this;
        this.checkAccountDataIsNull = function (account) { return __awaiter(_this, void 0, void 0, function () {
            var data, err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, this.provider.connection.getAccountInfo(account)];
                    case 1:
                        data = _a.sent();
                        return [2 /*return*/, data === null];
                    case 2:
                        err_1 = _a.sent();
                        throw new Error(err_1.toString());
                    case 3: return [2 /*return*/];
                }
            });
        }); };
        this.getProgram = function (programIdString) { return __awaiter(_this, void 0, void 0, function () {
            var programId, idl, data, err_2, program;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        try {
                            programId = AnchorClient.getPublicKey(programIdString);
                        }
                        catch (err) {
                            throw new Error(err.toString());
                        }
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, Program.fetchIdl(programId, this.provider)];
                    case 2:
                        data = _a.sent();
                        if (data !== null)
                            idl = data;
                        else
                            throw new Error("Idl Account has no data");
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _a.sent();
                        throw new Error(err_2.toString());
                    case 4:
                        program = new Program(idl, programId, this.provider);
                        return [2 /*return*/, program];
                }
            });
        }); };
        this.payerSign = function (tx, signers) { return __awaiter(_this, void 0, void 0, function () {
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        tx.feePayer = this.payer.publicKey;
                        _a = tx;
                        return [4 /*yield*/, this.provider.connection.getLatestBlockhash()];
                    case 1:
                        _a.recentBlockhash = (_b.sent()).blockhash;
                        tx = Transaction.from(tx.serialize({
                            verifySignatures: false,
                            requireAllSignatures: false,
                        }));
                        tx.partialSign(this.payer);
                        if (signers) {
                            signers.map(function (v) { return tx.partialSign(v); });
                        }
                        return [2 /*return*/, tx];
                }
            });
        }); };
        this.getPayerPublicKey = function () { return _this.payer.publicKey; };
        var payer = AnchorClient.getKeypair(payerUint8ArrayString);
        this.payer = payer;
        this.wallet = new NodeWallet(payer);
        this.endpoint = endpoint || "http://localhost:8899";
        this.provider = new AnchorProvider(new Connection(this.endpoint, { commitment: "confirmed" }), this.wallet, { commitment: "confirmed" });
    }
    AnchorClient.getPublicKey = function (publicKeyString) {
        try {
            var publicKey = new PublicKey(publicKeyString);
            return publicKey;
        }
        catch (err) {
            throw new Error("Not valid base58 encoded string");
        }
    };
    AnchorClient.getKeypair = function (uint8ArrayString) {
        try {
            var newKeypair = Keypair.fromSecretKey(Uint8Array.from(JSON.parse(uint8ArrayString)));
            return newKeypair;
        }
        catch (err) {
            throw new Error("Not valid uint8ArrayString");
        }
    };
    AnchorClient.getPublicKeys = function (publicKeyStrings) {
        var result = {};
        for (var _i = 0, _a = Object.entries(publicKeyStrings); _i < _a.length; _i++) {
            var _b = _a[_i], key = _b[0], value = _b[1];
            try {
                result[key] = new PublicKey(value);
            }
            catch (err) {
                throw new Error("Not valid base58 encoded string");
            }
        }
        return result;
    };
    AnchorClient.getATAAddress = function (mint, owner, allowOwnerOffCurve) {
        try {
            var ata = getAssociatedTokenAddressSync(mint, owner, allowOwnerOffCurve);
            return ata;
        }
        catch (err) {
            throw new Error(err.toString());
        }
    };
    return AnchorClient;
}());
export { AnchorClient };
export var getMetadataAddress = function (mint) {
    return web3.PublicKey.findProgramAddressSync([Buffer.from("metadata"), METADATA_PROGRAM_ID.toBuffer(), mint.toBuffer()], METADATA_PROGRAM_ID)[0];
};
//# sourceMappingURL=utils.js.map