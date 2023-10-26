import { NextRequest, NextResponse } from "next/server";
import { Profile } from "@genie-web3/svm-integration";
import { getGenie } from "@/app/lib/genie";
import { Keypair, PublicKey } from "@solana/web3.js";

export async function POST(request: NextRequest) {
  try{ const body = await request.json();
  const initialAuth = Keypair.fromSecretKey(
    Uint8Array.from(JSON.parse(body.initialAuth)),
  );

  const genie = await getGenie();

  const profile = new Profile(genie, initialAuth.publicKey);
  const txId = await profile.initialize(initialAuth);
  console.log(txId);

  return NextResponse.json({ success: true, txId: txId });}
  catch(err){
    return NextResponse.json({success:false, txId: JSON.stringify(err)})
  }
 
}
