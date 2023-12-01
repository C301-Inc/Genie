import sys
import time
from utils.api_call import send_token
from dotenv import load_dotenv

load_dotenv()

fail = 0
for i in range(100):
    success = send_token(sys.argv[1], 
                "Solana", 
                "So11111111111111111111111111111111111111112",
                0.00000001,
                "tA4fhDD2C3xqJ2cSo6wiDAdkaeBgkTaWJpDESv7ZMKj",
                ""
    )
    print(success)
    if success is None:
        fail += 1

print(fail)
