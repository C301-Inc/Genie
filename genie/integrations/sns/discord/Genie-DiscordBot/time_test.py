import sys
import time
from utils.api_call import get_user_tokens
from dotenv import load_dotenv

load_dotenv()

time_list = []
for i in range(1000):
    start = time.time()
    get_user_tokens(sys.argv[1], "Solana")
    end = time.time()
    time_list.append(end-start)

result = sum(time_list) / 1000

print(result)
