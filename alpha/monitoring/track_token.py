from time import time
from pydantic import BaseModel, model_validator

'''The script here manages the tokens based on a few parameters such as liqudity, volume, past price movement etc.. '''


class Data(BaseModel):
    volume : float
    price_change_5m : float


class TokenTracker(BaseModel):
        token_id : str
        data : Data
        start_time : float = time()
        score : float =  0
        is_expired: bool = False

        @model_validator(mode="after")
        def calculate_score(self):
            """Calculate token score based on volume and price change"""
            self.score = self.data.get('volume', 0) * abs(self.data.get('price_change_5m', 0))
            self.is_expired = self.is_expired(ttl=900)
            return self

        
        def is_expired(self, ttl=900):  # 15 mins TTL
            return time() - self.start_time > ttl
        
        def get_result(self) -> (float, bool): #to be fixed
             return self.score, self.is_expired()