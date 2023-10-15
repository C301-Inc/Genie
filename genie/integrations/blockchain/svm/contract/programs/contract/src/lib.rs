use anchor_lang::prelude::*;

declare_id!("DcFiN7rdT7MRJJgRLJYcriTn2NgemPn6iqz9X2uqw4fK");

#[program]
pub mod contract {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize {}
