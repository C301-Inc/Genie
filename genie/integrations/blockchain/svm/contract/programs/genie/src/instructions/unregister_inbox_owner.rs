use crate::{cmp_pubkeys, GenieError, Inbox, Profile};
use anchor_lang::prelude::*;

#[derive(Accounts)]
pub struct UnregisterInboxOwner<'info> {
    payer: Signer<'info>,
    #[account(mut)]
    pub inbox: Account<'info, Inbox>,
    pub initial_auth_inbox: Signer<'info>,
    pub profile: Account<'info, Profile>,
    pub initial_auth_profile: Signer<'info>,
}

pub fn unregister_inbox_owner(ctx: Context<UnregisterInboxOwner>) -> Result<()> {
    // 0. check inbox profile_owner is not None
    // 1. check profile auth is initial_auth or user_auth : profile.auth.is_initial_valid
    // 2. check required auth is valid
    // 3. change inbox.owner_profile

    if ctx.accounts.inbox.owner_profile == None {
        return err!(GenieError::OwnerNotExist);
    }

    // check auth_profile === initial_auth
    if !cmp_pubkeys(
        &ctx.accounts.profile.auth.initial_auth,
        &ctx.accounts.initial_auth_profile.key(),
    ) {
        return err!(GenieError::InvalidAuth);
    }

    ctx.accounts.inbox.owner_profile = None;

    Ok(())
}
