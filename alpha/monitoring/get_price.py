from dexscreener import DexscreenerClient
from telegram import token_safety
from pydantic import BaseModel
import asyncio
import pickle
from ollama import chat, ChatResponse

''' A defenition to get the price of the token and save it to a time series data base. The price is updated through various sources: dexscreener, telegram etc.'''

# with open('alpha/ca.pickle', 'rb') as f:
#             addy = pickle.load(f)


class getPrice(BaseModel):
    ca : str

    async def get_from_dex(self):
        pair = await DexscreenerClient.search_pairs(self.ca)
        price = pair.price_usd

    async def get_from_telegram(self):
        message = await token_safety.SafetyCheck(ca=self.ca).get_details()
        messages = [
        {
            'role': 'user',
            'content': f'respond output with keys in lowercase in json only : {message}',
        },
        ]

        response = chat('llama3.2', messages=messages)
        # print(messages)
        return response['message']['content']


# get = getPrice(ca=addy)

# asyncio.get_event_loop().run_until_complete(get.get_from_telegram())