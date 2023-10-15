use crate::Genie;
use anchor_lang::prelude::*;
use anchor_spl::{
    metadata::Metadata,
    token::{Mint, Token},
};

#[derive(Accounts)]
pub struct InitializeGenie<'info> {
    /// genie's authority SHOULD BE multisig
    #[account(
    init,
    seeds = [b"genie".as_ref(),authority.key().as_ref()],
    payer = payer,
    bump,
    space= 8 + Genie::INIT_SPACE
    )]
    pub genie: Account<'info, Genie>,
    #[account(
    init,
    seeds = [b"genie_profile".as_ref(),genie.key().as_ref()],
    payer = payer,
    bump,
    mint::decimals = 0,
    mint::authority = genie,
    mint::freeze_authority = genie
    )]
    pub profile_mark: Account<'info, Mint>,
    /// CHECK: THIS ACCOUNT IS METADATA ACCOUNT OF GENIE MARK
    /// ["metadata".as_bytes(), program_id.as_ref(), genie_mark.as_ref()], program_id = metadata_program
    #[account(mut)]
    pub profile_metadata: UncheckedAccount<'info>,
    #[account(
    init,
    seeds = [b"genie_inbox".as_ref(),genie.key().as_ref()],
    payer = payer,
    bump,
    mint::decimals = 0,
    mint::authority = genie,
    mint::freeze_authority = genie
    )]
    pub inbox_mark: Account<'info, Mint>,
    /// CHECK: THIS ACCOUNT IS METADATA ACCOUNT OF GENIE MARK
    /// ["metadata".as_bytes(), program_id.as_ref(), genie_mark.as_ref()], program_id = metadata_program
    #[account(mut)]
    pub inbox_metadata: UncheckedAccount<'info>,
    /// CHECK: THIS ACCOUNT SHOULD BE SIGNER OF MULTISIG (using single signer for testing)
    pub authority: Signer<'info>,
    #[account(mut)]
    pub payer: Signer<'info>,
    pub system_program: Program<'info, System>,
    token_program: Program<'info, Token>,
    pub metadata_program: Program<'info, Metadata>,
    pub rent: Sysvar<'info, Rent>,
}
