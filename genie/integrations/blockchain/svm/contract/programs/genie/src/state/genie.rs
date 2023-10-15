use anchor_lang::prelude::*;

#[account]
#[derive(Default, Debug, InitSpace)]
pub struct Genie {
    /// THIS SHOULD BE MULTISIG SIGNER
    pub authority: Pubkey, //32
    /// METADATA for token marking represent GENIE profile account
    #[max_len(200)]
    pub profile_metadata_uri: String, //4 + 200
    /// METADATA for token marking represent GENIE Inbox account
    #[max_len(200)]
    pub inbox_metadata_uri: String, //4 + 200
    /// ADDITIONAL INFO USING GENIE LAYER
    #[max_len(200)]
    pub external_uri: String, //4 + 200
    pub bump: u8, // 1
}
