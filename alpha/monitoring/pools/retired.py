from pydantic import BaseModel, model_validator
from db.db_pass_retired import passToDb
import time
from collections import deque
import threading
import schedule



'''This section represents the retired pool that keeps on tracking the prices 
of the retired tokens. The prices are tracked on to a time series database'''

class RetiredTracking(BaseModel):
    tokens : deque
    token_ids : deque
    tracking_interval : int


    # @model_validator(mode="after")
    def price_tracking(self):
        def job():
            for token,token_id in zip(self.tokens,self.token_ids):
                price = self.get_price(token_id)
                passToDb(token, price).price_writer()
        
        schedule.every(self.tracking_interval).seconds.do(job)

        # Start scheduler in background thread
        thread = threading.Thread(target=self._run_scheduler, daemon=True)
        thread.start()
        return self
    
    def _run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    def get_price(self, token_id):
        ## to be implemented
        price = get_price() 
        return price


