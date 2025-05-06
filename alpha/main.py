from get_tokens.from_dex import get_dexscreener
from telegram import token_safety
import asyncio


safety = {}

async def main():
    token_addresses, token_price_details =  await get_dexscreener.GetTokens.main()
    for address in token_addresses:
        safety[address] = await token_safety.SafetyCheck(ca=address).main()
        

asyncio.get_event_loop().run_until_complete(main())