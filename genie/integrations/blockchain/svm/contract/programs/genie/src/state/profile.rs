use anchor_lang::prelude::*;

#[derive(AnchorSerialize, AnchorDeserialize, Default, Debug, Clone, InitSpace)]
pub struct Auth {
    pub initial_auth: Pubkey,   // 32
    pub is_initial_valid: bool, // 1
    #[max_len(10)]
    pub auth_list: Vec<Pubkey>, // 4 + 10 * 32
}

impl Auth {
    pub fn initialize<'info>(initial_auth: Pubkey) -> Result<Auth> {
        Ok(Auth {
            initial_auth: initial_auth,
            is_initial_valid: true,
            auth_list: Vec::with_capacity(46),
        })
    }
}
#[account]
#[derive(Default, Debug, InitSpace)]
pub struct Profile {
    pub auth: Auth, // 32 + 1 + 4 + 32*10
    pub bump: u8,   // 1
}

impl Profile {
    pub fn initialize<'info>(&mut self, initial_auth: Pubkey, bump: u8) -> Result<&Profile> {
        self.auth = Auth::initialize(initial_auth)?;
        self.bump = bump;
        Ok(self)
    }
}
