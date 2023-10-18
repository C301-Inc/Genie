use anchor_lang::prelude::*;

pub mod error;
pub mod instructions;
pub mod state;
pub mod utils;

pub use error::*;
pub use instructions::*;
pub use state::*;
pub use utils::*;

declare_id!("DcFiN7rdT7MRJJgRLJYcriTn2NgemPn6iqz9X2uqw4fK");

#[program]
pub mod genie {
    use super::*;

    pub fn initialize_genie(
        ctx: Context<InitializeGenie>,
        profile_metadata_uri: String,
        inbox_metadata_uri: String,
        external_uri: String,
    ) -> Result<()> {
        let genie_bump = ctx.bumps.genie;
        instructions::initialize_genie(
            ctx,
            profile_metadata_uri,
            inbox_metadata_uri,
            external_uri,
            genie_bump,
        )?;
        Ok(())
    }

    pub fn initialize_profile(ctx: Context<InitializeProfile>) -> Result<()> {
        let profile_bump = ctx.bumps.profile;
        instructions::initialize_profile(ctx, profile_bump)?;
        Ok(())
    }

    pub fn initialize_inbox(
        ctx: Context<InitializeInbox>,
        platform: String,
        primary_key: String,
    ) -> Result<()> {
        let inbox_bump = ctx.bumps.inbox;
        instructions::initialize_inbox(ctx, platform, primary_key, inbox_bump)?;
        Ok(())
    }

    pub fn register_inbox_owner(ctx: Context<RegisterInboxOwner>) -> Result<()> {
        instructions::register_inbox(ctx)?;
        Ok(())
    }

    pub fn unregister_inbox_owner(ctx: Context<UnregisterInboxOwner>) -> Result<()> {
        instructions::unregister_inbox_owner(ctx)?;
        Ok(())
    }
    pub fn send_token(ctx: Context<SendToken>, amount: u64) -> Result<()> {
        instructions::send_token(ctx, amount)?;
        Ok(())
    }
}
