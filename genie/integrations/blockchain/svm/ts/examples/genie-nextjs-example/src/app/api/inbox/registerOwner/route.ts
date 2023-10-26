import { NextRequest, NextResponse } from "next/server";
import { Inbox } from "@genie-web3/svm-integration";
import { getGenie } from "@/app/lib/genie";
import { Keypair, PublicKey } from "@solana/web3.js";

export async function POST(request: NextRequest) {
    try{
const body = await request.json();
  const initialAuthInbox = Keypair.fromSecretKey(
    Uint8Array.from(JSON.parse(body.initialAuthInbox)),
  );
  const initialAuthProfile = Keypair.fromSecretKey(
    Uint8Array.from(JSON.parse(body.initialAuthProfile)),
  );


  const genie = await getGenie();

  const inbox = new Inbox(genie, initialAuthInbox.publicKey);
  const txId = await inbox.registerOwner(initialAuthInbox, initialAuthProfile)

  return NextResponse.json({ success: true, txId: txId });
    }
    catch(err){
        return NextResponse.json({success:false, txId: JSON.stringify(err)})
    }
  
}
