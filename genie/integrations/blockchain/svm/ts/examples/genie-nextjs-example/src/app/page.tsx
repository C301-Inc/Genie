'use client'
import Image from 'next/image'
import { useCallback, useState, useEffect, useRef } from 'react'
import {
  TOKEN_PROGRAM_ID,
  getAssociatedTokenAddressSync,
  createAssociatedTokenAccountInstruction,
  createTransferInstruction
} from '@solana/spl-token'
import { useConnection, useWallet } from '@solana/wallet-adapter-react'
import {
  PublicKey,
  TransactionInstruction,
  Transaction,
  SystemProgram
} from '@solana/web3.js'
import { getErrorMessage } from './utils'

export default function Home() {
  const [inboxKey, setInboxKey] = useState<string>('')
  const [tokenList, setTokenList] = useState<
    Array<{ mint: string; amount: string; decimals: string; selected: boolean }>
  >([])
  const [amount, setAmount] = useState<string>('0')

  const conn = useConnection()
  const wallet = useWallet()

  const sendToken = async (mint: string) => {
    try {
      if (mint === 'Native Solana') {
        console.log('here')
        const destPublicKey = new PublicKey(inboxKey)
        const transaction = new Transaction().add(
          SystemProgram.transfer({
            //@ts-ignore
            fromPubkey: wallet.publicKey,
            toPubkey: destPublicKey,
            lamports: BigInt(amount)
          })
        )
        //@ts-ignore
        transaction.feePayer = wallet.publicKey
        wallet.sendTransaction(transaction, conn.connection)
      } else {
        const mintToken = new PublicKey(mint)

        const fromTokenAccount = getAssociatedTokenAddressSync(
          mintToken,
          //@ts-ignore
          wallet.publicKey
        )

        const destPublicKey = new PublicKey(inboxKey)

        // Get the derived address of the destination wallet which will hold the custom token
        const associatedDestinationTokenAddr = getAssociatedTokenAddressSync(
          mintToken,
          destPublicKey
        )

        const receiverAccount = await conn.connection.getAccountInfo(
          associatedDestinationTokenAddr
        )

        const instructions: TransactionInstruction[] = []

        if (receiverAccount === null) {
          instructions.push(
            createAssociatedTokenAccountInstruction(
              //@ts-ignore
              wallet.publicKey,
              associatedDestinationTokenAddr,
              destPublicKey,
              mintToken
            )
          )
        }

        instructions.push(
          createTransferInstruction(
            fromTokenAccount,
            associatedDestinationTokenAddr,
            //@ts-ignore
            wallet.publicKey,
            BigInt(amount)
          )
        )

        const transaction = new Transaction().add(...instructions)
        //@ts-ignore
        transaction.feePayer = wallet.publicKey
        wallet.sendTransaction(transaction, conn.connection)
      }
    } catch (err) {}
  }

  const onChangeKey = (e: any) => {
    setInboxKey(e)
    return
  }

  const onChangeAmount = (e: any) => {
    setAmount(e)
    return
  }

  useEffect(() => {
    const getTokens = async () => {
      const list = await conn.connection
        //@ts-ignore
        .getParsedTokenAccountsByOwner(wallet.publicKey, {
          programId: TOKEN_PROGRAM_ID
        })
        .then((res) =>
          res.value
            .filter((f) => {
              return f.account.data.parsed.info.tokenAmount.decimals !== 0
            })
            .filter(
              (f) => f.account.data.parsed.info.tokenAmount.amount !== '0'
            )
            .map((v) => {
              return {
                mint: v.account.data.parsed.info.mint,
                amount: v.account.data.parsed.info.tokenAmount.amount,
                decimals: v.account.data.parsed.info.tokenAmount.decimals,
                selected: false
              }
            })
        )
        .catch((error) => {
          throw new Error(getErrorMessage(error))
        })

      const solanaBalance = await conn.connection
        //@ts-ignore
        .getBalance(wallet.publicKey)
        .then((res) => {
          return {
            mint: 'Native Solana',
            amount: res.toString(),
            decimals: '9',
            selected: false
          }
        })
      list.splice(0, 0, solanaBalance)
      setTokenList(list)
    }
    getTokens()
  }, [wallet.publicKey])

  const setSelectedToken = (i: number) => {
    if (tokenList.length > i) {
      tokenList.map((v, j) => {
        if (j === i) {
          v.selected = true
          return v
        } else {
          v.selected = false
          return v
        }
      })
      setTokenList([...tokenList])
    }
  }

  return (
    <main
      style={{ display: 'flex', flexDirection: 'column', margin: '12px 12px' }}>
      <div style={{ display: 'flex', flexDirection: 'row', gap: '10px' }}>
        <input
          style={{ width: '80%', height: '40px' }}
          placeholder="Enter Inbox Key Here"
          onChange={(e) => {
            onChangeKey(e.target.value)
          }}
          value={inboxKey}></input>{' '}
        <button
          style={{ width: '20%' }}
          onClick={async () => {
            try {
              await sendToken(
                tokenList.findLast((v) => v.selected === true)?.mint || ''
              )
            } catch (err) {
              alert('Token Not Selected')
            }
          }}>
          send
        </button>
      </div>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '12px',
          marginTop: '24px'
        }}>
        {tokenList.map((v, i) => {
          return (
            <div
              key={i}
              style={{
                display: 'flex',
                flexDirection: 'row',
                width: '100%',
                border: v.selected ? 'solid 2px blue' : 'solid 0.5px grey',
                height: '60px'
              }}
              onClick={() => {
                setSelectedToken(i)
              }}>
              <div style={{ width: '80%' }}>
                <div>{`Mint Address : ${v.mint}`}</div>
                <div>{`Current Amount : ${v.amount}`}</div>
                <div>{`Decimals : ${v.decimals}`}</div>
              </div>
              <div
                style={{
                  width: '20%',
                  height: '60px',
                  display: 'flex',
                  alignItems: 'center'
                }}>
                <input
                  disabled={!v.selected}
                  style={{}}
                  placeholder="Enter Send Amount"
                  value={v.selected ? amount : 'Not Selected'}
                  pattern="\d*"
                  onChange={(e) => {
                    onChangeAmount(e.target.value)
                  }}></input>
              </div>
            </div>
          )
        })}
      </div>
    </main>
  )
}
