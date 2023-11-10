use crate::Genie;
use anchor_lang::prelude::*;
use anchor_spl::metadata::{
    create_metadata_accounts_v3, mpl_token_metadata::types::DataV2, CreateMetadataAccountsV3,
};
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

pub fn initialize_genie(
    ctx: Context<InitializeGenie>,
    profile_metadata_uri: String,
    inbox_metadata_uri: String,
    external_uri: String,
    genie_bump: u8,
) -> Result<()> {
    ctx.accounts.genie.initialize(
        ctx.accounts.authority.key(),
        profile_metadata_uri,
        inbox_metadata_uri,
        external_uri,
        genie_bump,
    )?;

    create_profile_metadata(&ctx)?;
    create_inbox_metadata(&ctx)?;

    Ok(())
}

fn create_profile_metadata(ctx: &Context<InitializeGenie>) -> Result<()> {
    let bump = ctx.accounts.genie.bump;
    let authority_seeds = &[
        "genie".as_bytes(),
        &ctx.accounts.genie.authority.to_bytes(),
        &[bump],
    ];

    let cpi_program = ctx.accounts.metadata_program.to_account_info();
    let cpi_accounts = CreateMetadataAccountsV3 {
        metadata: ctx.accounts.profile_metadata.to_account_info(),
        mint: ctx.accounts.profile_mark.to_account_info(),
        mint_authority: ctx.accounts.genie.to_account_info(),
        payer: ctx.accounts.payer.to_account_info(),
        update_authority: ctx.accounts.genie.to_account_info(),
        system_program: ctx.accounts.system_program.to_account_info(),
        rent: ctx.accounts.rent.to_account_info(),
    };
    create_metadata_accounts_v3(
        CpiContext::new(cpi_program, cpi_accounts).with_signer(&[&authority_seeds[..]]),
        DataV2 {
            name: "GENIE Profile Account".to_string(),
            symbol: "GENIE".to_string(),
            uri: ctx.accounts.genie.profile_metadata_uri.clone(),
            seller_fee_basis_points: 0,
            creators: None,
            collection: None,
            uses: None,
        },
        true,
        true,
        None,
    )?;
    Ok(())
}

fn create_inbox_metadata(ctx: &Context<InitializeGenie>) -> Result<()> {
    let bump = ctx.accounts.genie.bump;
    let authority_seeds = &[
        "genie".as_bytes(),
        &ctx.accounts.genie.authority.to_bytes(),
        &[bump],
    ];

    let cpi_program = ctx.accounts.metadata_program.to_account_info();
    let cpi_accounts = CreateMetadataAccountsV3 {
        metadata: ctx.accounts.inbox_metadata.to_account_info(),
        mint: ctx.accounts.inbox_mark.to_account_info(),
        mint_authority: ctx.accounts.genie.to_account_info(),
        payer: ctx.accounts.payer.to_account_info(),
        update_authority: ctx.accounts.genie.to_account_info(),
        system_program: ctx.accounts.system_program.to_account_info(),
        rent: ctx.accounts.rent.to_account_info(),
    };
    create_metadata_accounts_v3(
        CpiContext::new(cpi_program, cpi_accounts).with_signer(&[&authority_seeds[..]]),
        DataV2 {
            name: "GENIE Inbox Account".to_string(),
            symbol: "GENIE".to_string(),
            uri: ctx.accounts.genie.inbox_metadata_uri.clone(),
            seller_fee_basis_points: 0,
            creators: None,
            collection: None,
            uses: None,
        },
        true,
        true,
        None,
    )?;
    Ok(())
}
