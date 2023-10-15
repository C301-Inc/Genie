use crate::{Genie, Profile};
use anchor_lang::prelude::*;
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{Mint, Token, TokenAccount},
};

#[derive(Accounts)]
pub struct InitializeProfile<'info> {
    #[account(
    init,
    seeds=[b"profile".as_ref(),initial_auth.key().as_ref()],
    payer= payer,
    bump,
    space= 8 + Profile::INIT_SPACE
    )]
    pub profile: Account<'info, Profile>,
    pub initial_auth: Signer<'info>,
    #[account(
    init,
    payer = payer,
    associated_token::mint = profile_mark,
    associated_token::authority = profile,
    )]
    pub profile_mark_account: Account<'info, TokenAccount>,
    #[account(mut)]
    pub profile_mark: Account<'info, Mint>,
    pub genie: Account<'info, Genie>,
    #[account(mut)]
    pub payer: Signer<'info>,
    pub token_program: Program<'info, Token>,
    associated_token_program: Program<'info, AssociatedToken>,
    system_program: Program<'info, System>,
    rent: Sysvar<'info, Rent>,
}
