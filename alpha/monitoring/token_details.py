from get_price import getPrice
from pydantic import BaseModel, model_validator
import asyncio
import json

class getTokenInfo(BaseModel):
    token_id : str
    token : str
    price : float = None
    market_cap : float = None
    liquidity : float = None
    dex : str = None

    @model_validator(mode="after")
    async def get_details_bana(self):
        details = await getPrice(ca=self.token_id).get_from_telegram()
        detials_json = json.loads(details)
        print(detials_json)
        self.price = detials_json["price"]
        self.market_cap = detials_json["market_cap"]
        self.liquidity = detials_json["liquidity"]
        self.token = detials_json["token"]
        self.dex = detials_json["dex"]

    @property
    def get_price(self):
        return self.price

    def get_mcap(self):
        return self.market_cap

    def get_liq(self):
        return self.liquidity
