use anchor_lang::prelude::*;

#[account]
#[derive(Default, Debug, InitSpace)]
pub struct Profile {
    pub auth: Auth, // 32 + 1 + 4 + 32*10
    pub bump: u8,   // 1
}

#[derive(AnchorSerialize, AnchorDeserialize, Default, Debug, Clone, InitSpace)]
pub struct Auth {
    pub initial_auth: Pubkey,   // 32
    pub is_initial_valid: bool, // 1
    #[max_len(10)]
    pub auth_list: Vec<Pubkey>, // 4 + 10 * 32
}
