## Getting Started

First, create .env file in the root of this directory
```
PAYER_KEY = <payer's secret key in Uint8 array format [22,135,...,35,125]>
GENIE_PROGRAM_ID = <Deployed Genie Program Id>
SOLANA_ENDPOINT = <Solana Rpc Endpoint>
GENIE_AUTHORITY = <Genie initialization secret key in Uint8 array format [22,135,...,35,125]>
```

Secondly, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
