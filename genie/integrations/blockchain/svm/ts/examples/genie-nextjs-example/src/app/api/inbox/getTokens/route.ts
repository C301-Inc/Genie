import { NextRequest, NextResponse } from 'next/server'
import { Inbox } from '@genie-web3/svm-integration'
import { getGenie } from '@/app/lib/genie'
import { Keypair, PublicKey } from '@solana/web3.js'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const initialAuth = Keypair.fromSecretKey(
      Uint8Array.from(JSON.parse(body.initialAuth))
    )

    const genie = await getGenie()

    const inbox = new Inbox(genie, initialAuth.publicKey)
    const list = await inbox.getTokens()

    return NextResponse.json({ success: true, list: list })
  } catch (err) {
    return NextResponse.json({ success: false, txId: JSON.stringify(err) })
  }
}
