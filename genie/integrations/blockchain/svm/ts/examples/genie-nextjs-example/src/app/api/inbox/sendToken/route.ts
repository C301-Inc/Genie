import { NextRequest, NextResponse } from 'next/server'
import { Inbox } from '@genie-web3/svm-integration'
import { getGenie } from '@/app/lib/genie'
import { Keypair, PublicKey } from '@solana/web3.js'
import { getErrorMessage } from '@/app/utils'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const initialAuthInbox = Keypair.fromSecretKey(
      Uint8Array.from(JSON.parse(body.initialAuthInbox))
    )
    const initialAuthProfile = Keypair.fromSecretKey(
      Uint8Array.from(JSON.parse(body.initialAuthProfile))
    )
    const mint = new PublicKey(body.mint)
    const receiver = new PublicKey(body.receiver)
    const genie = await getGenie()

    const inbox = new Inbox(genie, initialAuthInbox.publicKey)

    const txId = await inbox.sendToken(
      initialAuthProfile,
      receiver,
      mint,
      body.amount
    )

    return NextResponse.json({ success: true, txId: txId })
  } catch (err) {
    //@ts-ignore
    return NextResponse.json({ success: false, txId: getErrorMessage(err) })
  }
}
