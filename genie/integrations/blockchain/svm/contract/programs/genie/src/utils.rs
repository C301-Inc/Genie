use anchor_lang::prelude::*;
use solana_program::{
    program_memory::sol_memcmp,
    program_pack::{IsInitialized, Pack},
    pubkey::{Pubkey, PUBKEY_BYTES},
};

use crate::GenieError;

pub fn cmp_pubkeys(a: &Pubkey, b: &Pubkey) -> bool {
    sol_memcmp(a.as_ref(), b.as_ref(), PUBKEY_BYTES) == 0
}

pub fn assert_owned_by(account: &AccountInfo, owner: &Pubkey) -> Result<()> {
    if !cmp_pubkeys(account.owner, owner) {
        Err(GenieError::IncorrectOwnerProgram.into())
    } else {
        Ok(())
    }
}

pub fn assert_initialized<T: Pack + IsInitialized>(account_info: &AccountInfo) -> Result<T> {
    let account: T = T::unpack_unchecked(&account_info.data.borrow())?;
    if !account.is_initialized() {
        Err(GenieError::UninitializedAccount.into())
    } else {
        Ok(account)
    }
}

pub fn assert_not_allocated(account_info: &AccountInfo) -> Result<()> {
    if account_info.data_is_empty() {
        Ok(())
    } else {
        Err(GenieError::InitializedAccount.into())
    }
}

pub fn add_item_to_vector<T: Copy + Clone>(new_item: &T, list: &mut Vec<T>) -> bool {
    if list.len() < 10 {
        list.push(*new_item);
        true
    } else {
        false
    }
}
pub fn remove_item_from_vector<T: Copy + Clone + PartialEq>(
    remove_item: &T,
    list: &mut Vec<T>,
) -> bool {
    if list.contains(remove_item) {
        list.retain(|item| *item != *remove_item);
        true
    } else {
        false
    }
}

pub fn check_item_in_vector<T: Eq + Copy + Clone>(item: &T, list: &[T]) -> bool {
    list.iter().any(|&i| i == *item)
}

pub fn check_pubkey_in_vector(item: &Pubkey, list: &[Pubkey]) -> bool {
    list.iter().any(|&i| cmp_pubkeys(&i, &item))
}
#[test]
fn check_keys_equal() {
    let key1 = Pubkey::new_unique();
    assert!(cmp_pubkeys(&key1, &key1));
}

#[test]
fn check_vector_push() {
    let key1 = Pubkey::new_unique();
    let key2 = Pubkey::new_unique();
    let key3 = Pubkey::new_unique();
    let key4 = Pubkey::new_unique();
    let key5 = Pubkey::new_unique();

    let mut list: Vec<Pubkey> = Vec::new();
    assert!(add_item_to_vector(&key1, &mut list));
    assert!(add_item_to_vector(&key2, &mut list));
    assert!(add_item_to_vector(&key3, &mut list));
    assert!(add_item_to_vector(&key4, &mut list));
    assert!(add_item_to_vector(&key5, &mut list));

    assert_eq!(list[0], key1);
    assert_eq!(list[1], key2);
    assert_eq!(list[2], key3);
    assert_eq!(list[3], key4);
    assert_eq!(list[4], key5);
}

#[test]
fn check_item_in_vector_fn() {
    let key1 = Pubkey::new_unique();
    let key2 = Pubkey::new_unique();
    let key3 = Pubkey::new_unique();
    let key4 = Pubkey::new_unique();
    let key5 = Pubkey::new_unique();
    let key6 = Pubkey::new_unique();
    let mut list: Vec<Pubkey> = Vec::new();
    assert!(add_item_to_vector(&key1, &mut list));
    assert!(add_item_to_vector(&key2, &mut list));
    assert!(add_item_to_vector(&key3, &mut list));
    assert!(add_item_to_vector(&key4, &mut list));
    assert!(add_item_to_vector(&key5, &mut list));

    assert_eq!(check_item_in_vector(&key1, &list), true);
    assert_ne!(check_item_in_vector(&key6, &list), true);

    assert_eq!(check_pubkey_in_vector(&key1, &list), true);
    assert_ne!(check_pubkey_in_vector(&key6, &list), true);
}

#[test]
fn remove_item_in_vector_fn() {
    let key1 = Pubkey::new_unique();
    let key2 = Pubkey::new_unique();
    let key3 = Pubkey::new_unique();
    let key4 = Pubkey::new_unique();
    let key5 = Pubkey::new_unique();

    let mut list: Vec<Pubkey> = Vec::new();
    assert!(add_item_to_vector(&key1, &mut list));
    assert!(add_item_to_vector(&key2, &mut list));
    assert!(add_item_to_vector(&key3, &mut list));
    assert!(add_item_to_vector(&key4, &mut list));
    assert!(add_item_to_vector(&key5, &mut list));

    assert_eq!(check_item_in_vector(&key1, &list), true);

    assert!(remove_item_from_vector(&key2, &mut list));
    assert!(remove_item_from_vector(&key4, &mut list));

    assert_eq!(check_pubkey_in_vector(&key2, &list), false);
    assert_eq!(check_pubkey_in_vector(&key4, &list), false);

    assert_eq!(list.len() == 3, true);
}
