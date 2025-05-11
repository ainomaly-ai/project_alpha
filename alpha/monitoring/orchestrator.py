from collections import deque
from time import time
from pydantic import BaseModel, model_validator
from track_token import TokenTracker, Data
from get_tokens.from_dex import get_dexscreener
from pools.active import ActiveTracking
from pools.retired import RetiredTracking
from get_price import getPrice
from db.db_pass import passToDb
import asyncio
import threading
import schedule

''' There are 3 pools: active_pool where the tokens are currently monitored, candidate_pool where the potential candidates
    are set in que, retired_pool where under performing tokens are moved to and discarded. All the token data are 
    at the same time set to the timeseries database '''

active_pool = deque(maxlen=10)
active_token_name = deque(maxlen=10)
candidate_pool = deque(maxlen=10)
retired_pool = deque(maxlen=10)
retired_token_name = deque(maxlen=10)

class Monitor(BaseModel):
    token_id: str = None
    liquidity: float = None
    volume: float = None
    price_change_5m: float = None
    price_change_24h: float = None
    price_check_interval: int = None
    score_check_interval: int = None
    
    def track_token(self):
        '''Function to add specific token to the tracking pool'''
        score, is_expired = TokenTracker(token_id=self.token_id, data= Data(volume = self.volume, price_change_5m = self.price_change_5m))
        return score, is_expired
    
    def active(self):
        ActiveTracking(active_pool,active_token_name)
        
    
    async def candidate(self):
        ''' For specific interval get list of potential candidates'''
        token_addresses, token_price_details =  await get_dexscreener.GetTokens.main()
        for token in candidate_pool:
            if token != token_addresses:
                candidate_pool.append(token)
        

    def retired(self, retired_token):
        '''Pass to retired candidates when coin doesn't score, but still tracks for 
        a while in case volume picks up'''
        retired_pool.append(active_pool.pop(retired_token))
        RetiredTracking(retired_pool, retired_token_name)
        

def monitor_tokens():
    Monitor
    for token in active_pool:  # Iterate over all tokens in active pool
        current_score, is_expired = Monitor(token).track_token()
        if is_expired:
            Monitor(token).retired()
            Monitor(candidate_pool.pop).active()   

        elif current_score < active_pool[token]['last_checked'] + Monitor(token).price_check_interval:
            Monitor(token).candidate()   

if len(candidate_pool) == 0:
    Monitor().candidate()
    for item in candidate_pool:
        active_pool.append(item)
else:
    for token in active_pool:
        schedule.every(Monitor(token).price_check_interval).seconds.do(monitor_tokens, token)
