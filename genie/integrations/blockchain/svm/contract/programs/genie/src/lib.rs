use anchor_lang::prelude::*;

pub mod instructions;
pub mod state;

pub use instructions::*;
pub use state::*;

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
        let genie_bump = *ctx.bumps.get("genie").unwrap();
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
        let profile_bump = *ctx.bumps.get("profile").unwrap();
        instructions::initialize_profile(ctx, profile_bump)?;
        Ok(())
    }

    pub fn initialize_inbox(
        ctx: Context<InitializeInbox>,
        platform: String,
        primary_key: String,
    ) -> Result<()> {
        let inbox_bump = *ctx.bumps.get("inbox").unwrap();
        instructions::initialize_inbox(ctx, platform, primary_key, inbox_bump)?;
        Ok(())
    }
}
