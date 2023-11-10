use crate::{cmp_pubkeys, GenieError, Inbox, Profile};
use anchor_lang::prelude::*;
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{transfer_checked, Mint, Token, TokenAccount, TransferChecked},
};

#[derive(Accounts)]
pub struct SendToken<'info> {
    #[account(mut)]
    pub payer: Signer<'info>,
    pub mint: Account<'info, Mint>,
    pub sender_profile_auth: Signer<'info>,
    pub sender_profile: Account<'info, Profile>,
    pub sender_inbox: Account<'info, Inbox>,
    #[account(mut)]
    pub sender_token_account: Account<'info, TokenAccount>,
    ///CHECK : receiver address
    pub receiver: UncheckedAccount<'info>,
    #[account(
    init_if_needed,
    payer = payer,
    associated_token::mint = mint,
    associated_token::authority = receiver
    )]
    pub receiver_token_account: Account<'info, TokenAccount>,
    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

pub fn send_token(ctx: Context<SendToken>, amount: u64) -> Result<()> {
    let bump = ctx.accounts.sender_inbox.bump;
    let authority_seeds = &[
        "inbox".as_bytes(),
        &ctx.accounts.sender_inbox.initial_auth.to_bytes(),
        &[bump],
    ];

    // 0. check wallet address is in the profile auth list
    // 1. send token to receiver inbox

    // check auth_profile === initial_auth
    if !cmp_pubkeys(
        &ctx.accounts.sender_profile.auth.initial_auth,
        &ctx.accounts.sender_profile_auth.key(),
    ) {
        return err!(GenieError::InvalidAuth);
    }

    // check inbox_owner === profile
    if !cmp_pubkeys(
        &ctx.accounts.sender_inbox.owner_profile.unwrap(),
        &ctx.accounts.sender_profile.key(),
    ) {
        return err!(GenieError::InvalidAuth);
    }

    let cpi_program = ctx.accounts.token_program.to_account_info();
    let cpi_accounts = TransferChecked {
        from: ctx.accounts.sender_token_account.to_account_info(),
        mint: ctx.accounts.mint.to_account_info(),
        to: ctx.accounts.receiver_token_account.to_account_info(),
        authority: ctx.accounts.sender_inbox.to_account_info(),
    };

    transfer_checked(
        CpiContext::new(cpi_program, cpi_accounts).with_signer(&[&authority_seeds[..]]),
        amount,
        ctx.accounts.mint.decimals,
    )?;

    Ok(())
}
