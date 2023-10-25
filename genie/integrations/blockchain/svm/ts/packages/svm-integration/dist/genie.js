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
import { web3 } from "@coral-xyz/anchor";
import { AnchorClient, getMetadataAddress, METADATA_PROGRAM_ID, TOKEN_PROGRAM_ID, } from "./utils";
var Genie = /** @class */ (function () {
    function Genie(authority, payer, programId, endpoint) {
        this.isInitialized = false;
        this.authority = authority;
        this.programId = programId;
        var client = new AnchorClient(payer.secretKey.toString(), endpoint);
    }
    Object.defineProperty(Genie.prototype, "key", {
        get: function () {
            return this.isInitialized
                ? this.getGenieAddress(this.authority.publicKey)
                : undefined;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Genie.prototype, "profileMark", {
        get: function () {
            return this.key
                ? web3.PublicKey.findProgramAddressSync([Buffer.from("genie_profile"), this.key.toBuffer()], this.programId)[0]
                : undefined;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Genie.prototype, "inboxMark", {
        get: function () {
            return this.key
                ? web3.PublicKey.findProgramAddressSync([Buffer.from("genie_inbox"), this.key.toBuffer()], this.programId)[0]
                : undefined;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Genie.prototype, "program", {
        get: function () {
            var _this = this;
            return (function () { return __awaiter(_this, void 0, void 0, function () {
                var program;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, this.client
                                .getProgram(this.programId.toBase58())
                                .catch(function () { return undefined; })];
                        case 1:
                            program = _a.sent();
                            return [2 /*return*/, program];
                    }
                });
            }); })();
        },
        enumerable: false,
        configurable: true
    });
    Genie.prototype.initialize = function (programId, profileMarkLink, inboxMarkLink, webpage) {
        if (profileMarkLink === void 0) { profileMarkLink = "https://arweave.net/5XNlZK1agbCZgdJS50TwEl9SG-mhz-rndidoFi37Hzc"; }
        if (inboxMarkLink === void 0) { inboxMarkLink = "https://arweave.net/JbzEfZANGNoLIzP35Yj7ziFWKUrkQWhstehjS8l3OjU"; }
        if (webpage === void 0) { webpage = "https://www.geniebridge.link"; }
        return __awaiter(this, void 0, void 0, function () {
            var program, genieData, tx, err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 4, , 5]);
                        return [4 /*yield*/, this.program];
                    case 1:
                        program = _a.sent();
                        if (program === undefined) {
                            throw new Error("Program not initialized");
                        }
                        if (this.key === undefined ||
                            this.profileMark === undefined ||
                            this.inboxMark === undefined) {
                            throw new Error("genie not setted");
                        }
                        return [4 /*yield*/, program.account.genie
                                .fetch(this.key)
                                .then(function (res) { return res; })
                                .catch(function (err) { return undefined; })];
                    case 2:
                        genieData = _a.sent();
                        if (genieData !== undefined) {
                            this.isInitialized = true;
                            return [2 /*return*/, this.key];
                        }
                        return [4 /*yield*/, program.methods
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
                                rent: web3.SYSVAR_RENT_PUBKEY,
                            })
                                .signers([this.authority])
                                .rpc({ skipPreflight: true })
                                .then(function (res) { return res; })
                                .catch(function (error) {
                                throw new Error("genie initialization failed");
                            })];
                    case 3:
                        tx = _a.sent();
                        this.isInitialized = true;
                        return [2 /*return*/, this.key];
                    case 4:
                        err_1 = _a.sent();
                        throw new Error(err_1);
                    case 5: return [2 /*return*/];
                }
            });
        });
    };
    Genie.prototype.getGenieAddress = function (authority) {
        return this.programId
            ? web3.PublicKey.findProgramAddressSync([Buffer.from("genie"), authority.toBuffer()], this.programId)[0]
            : undefined;
    };
    return Genie;
}());
export default Genie;
//# sourceMappingURL=genie.js.map