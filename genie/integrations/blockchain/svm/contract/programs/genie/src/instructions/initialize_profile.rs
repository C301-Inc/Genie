use crate::{Genie, Profile};
use anchor_lang::prelude::*;
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{freeze_account, mint_to, FreezeAccount, Mint, MintTo, Token, TokenAccount},
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

pub fn initialize_profile(ctx: Context<InitializeProfile>, profile_bump: u8) -> Result<()> {
    ctx.accounts
        .profile
        .initialize(ctx.accounts.initial_auth.key(), profile_bump)?;

    print_and_freeze_mark(ctx)?;

    Ok(())
}

fn print_and_freeze_mark(ctx: Context<InitializeProfile>) -> Result<()> {
    // mint mark (sbt) for social account
    let bump = ctx.accounts.genie.bump;
    let authority_seeds = &[
        "genie".as_bytes(),
        &ctx.accounts.genie.authority.to_bytes(),
        &[bump],
    ];

    let cpi_program = ctx.accounts.token_program.to_account_info();
    let cpi_accounts = MintTo {
        mint: ctx.accounts.profile_mark.to_account_info(),
        to: ctx.accounts.profile_mark_account.to_account_info(),
        authority: ctx.accounts.genie.to_account_info(),
    };

    mint_to(
        CpiContext::new(cpi_program, cpi_accounts).with_signer(&[&authority_seeds[..]]),
        1,
    )?;

    // freeze mark (sbt) for social account
    let bump = ctx.accounts.genie.bump;
    let authority_seeds = &[
        "genie".as_bytes(),
        &ctx.accounts.genie.authority.to_bytes(),
        &[bump],
    ];
    let cpi_program = ctx.accounts.token_program.to_account_info();
    let cpi_accounts = FreezeAccount {
        account: ctx.accounts.profile_mark_account.to_account_info(),
        mint: ctx.accounts.profile_mark.to_account_info(),
        authority: ctx.accounts.genie.to_account_info(),
    };

    freeze_account(
        CpiContext::new(cpi_program, cpi_accounts).with_signer(&[&authority_seeds[..]]),
    )?;

    Ok(())
}
