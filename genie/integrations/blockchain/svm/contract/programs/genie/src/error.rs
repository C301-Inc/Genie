use anchor_lang::prelude::*;

#[error_code]
pub enum GenieError {
    #[msg("Account does not have correct owner Program")]
    IncorrectOwnerProgram,
    #[msg("Account is not initialized")]
    UninitializedAccount,
    #[msg("Account is already initialized")]
    InitializedAccount,
    #[msg("Auth account is not valid")]
    InvalidAuth,
    #[msg("Inbox already has owner")]
    OwnerExist,
    #[msg("Inbox has no owner")]
    OwnerNotExist,
    #[msg("Auth already in auth list")]
    DuplicateAuth,
    #[msg("Not Enough balance to send")]
    NotEnoughBalance,
}
