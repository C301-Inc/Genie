use crate::{Genie, Inbox};
use anchor_lang::prelude::*;
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{freeze_account, mint_to, FreezeAccount, Mint, MintTo, Token, TokenAccount},
};

#[derive(Accounts)]
pub struct InitializeInbox<'info> {
    #[account(
    init,
    seeds=[b"inbox".as_ref(),initial_auth.key().as_ref()],
    payer= payer,
    bump,
    space= 8 + Inbox::INIT_SPACE
    )]
    pub inbox: Account<'info, Inbox>,
    pub initial_auth: Signer<'info>,
    #[account(
    init,
    payer = payer,
    associated_token::mint = inbox_mark,
    associated_token::authority = inbox,
    )]
    pub inbox_mark_account: Account<'info, TokenAccount>,
    #[account(mut)]
    pub inbox_mark: Account<'info, Mint>,
    pub genie: Account<'info, Genie>,
    #[account(mut)]
    pub payer: Signer<'info>,
    pub token_program: Program<'info, Token>,
    associated_token_program: Program<'info, AssociatedToken>,
    system_program: Program<'info, System>,
    rent: Sysvar<'info, Rent>,
}

pub fn initialize_inbox(
    ctx: Context<InitializeInbox>,
    platform: String,
    primary_key: String,
    inbox_bump: u8,
) -> Result<()> {
    ctx.accounts.inbox.initialize(
        platform,
        primary_key,
        ctx.accounts.initial_auth.key(),
        inbox_bump,
        None,
    )?;

    print_and_freeze_mark(ctx)?;

    Ok(())
}

fn print_and_freeze_mark(ctx: Context<InitializeInbox>) -> Result<()> {
    // mint mark (sbt) for platform inbox
    let bump = ctx.accounts.genie.bump;
    let authority_seeds = &[
        "genie".as_bytes(),
        &ctx.accounts.genie.authority.to_bytes(),
        &[bump],
    ];

    let cpi_program = ctx.accounts.token_program.to_account_info();
    let cpi_accounts = MintTo {
        mint: ctx.accounts.inbox_mark.to_account_info(),
        to: ctx.accounts.inbox_mark_account.to_account_info(),
        authority: ctx.accounts.genie.to_account_info(),
    };

    mint_to(
        CpiContext::new(cpi_program, cpi_accounts).with_signer(&[&authority_seeds[..]]),
        1,
    )?;

    // freeze mark (sbt) for platform inbox
    let bump = ctx.accounts.genie.bump;
    let authority_seeds = &[
        "genie".as_bytes(),
        &ctx.accounts.genie.authority.to_bytes(),
        &[bump],
    ];
    let cpi_program = ctx.accounts.token_program.to_account_info();
    let cpi_accounts = FreezeAccount {
        account: ctx.accounts.inbox_mark_account.to_account_info(),
        mint: ctx.accounts.inbox_mark.to_account_info(),
        authority: ctx.accounts.genie.to_account_info(),
    };

    freeze_account(
        CpiContext::new(cpi_program, cpi_accounts).with_signer(&[&authority_seeds[..]]),
    )?;

    Ok(())
}
