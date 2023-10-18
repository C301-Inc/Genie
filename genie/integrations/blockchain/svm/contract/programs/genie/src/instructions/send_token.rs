use crate::{check_pubkey_in_vector, GenieError, Inbox, Profile};
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
    pub sender_profile: Account<'info, Profile>,
    pub sender_wallet: Signer<'info>,
    #[account(mut)]
    pub sender_token_account: Account<'info, TokenAccount>,
    pub receiver_inbox: Account<'info, Inbox>,
    #[account(
    init_if_needed,
    payer = payer,
    associated_token::mint = mint,
    associated_token::authority = receiver_inbox
    )]
    pub receiver_token_account: Account<'info, TokenAccount>,
    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

pub fn send_token(ctx: Context<SendToken>, amount: u64) -> Result<()> {
    // 0. check wallet address is in the profile auth list
    // 1. send token to receiver inbox

    //user has not registered their auth wallet
    // if ctx.accounts.sender_profile.auth.is_initial_valid {
    //     return err!(GenieError::InvalidAuth);
    // } else {
    //     // check send_wallet is in auth_list
    //     if !check_pubkey_in_vector(
    //         &ctx.accounts.sender_wallet.key(),
    //         &ctx.accounts.sender_profile.auth.auth_list,
    //     ) {
    //         return err!(GenieError::InvalidAuth);
    //     }
    // }

    let cpi_program = ctx.accounts.token_program.to_account_info();
    let cpi_accounts = TransferChecked {
        from: ctx.accounts.sender_token_account.to_account_info(),
        mint: ctx.accounts.mint.to_account_info(),
        to: ctx.accounts.receiver_token_account.to_account_info(),
        authority: ctx.accounts.sender_wallet.to_account_info(),
    };

    transfer_checked(
        CpiContext::new(cpi_program, cpi_accounts),
        amount,
        ctx.accounts.mint.decimals,
    )?;

    Ok(())
}
