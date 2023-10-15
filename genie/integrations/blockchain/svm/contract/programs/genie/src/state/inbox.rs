use anchor_lang::prelude::*;

#[account]
#[derive(Default, Debug, InitSpace)]
pub struct Inbox {
    /// This value never change after initialization
    /// web2 platform name
    /// ex) discord, twitter, telegram
    #[max_len(100)]
    pub platform: String, // 4 + 200
    /// This value never change after initialization
    /// web2 platform's user PK
    /// ex) handle
    #[max_len(200)]
    pub primary_key: String, // 4 + 200
    /// This value never change after initialization
    pub initial_auth: Pubkey, // 32
    pub bump: u8,                      // 1
    pub owner_profile: Option<Pubkey>, // 1 + 32
}
