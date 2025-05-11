import influxdb_client, os, time
import threading
from alpha.monitoring.token_details import getTokenInfo
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from pydantic import BaseModel

# InfluxDB configuration

INFLUX_URL = "http://localhost:8086"
token = os.environ.get("INFLUXDB_TOKEN")
INFLUX_ORG = "crypto"
BUCKET = "pricedata_retired"

client = InfluxDBClient(url=INFLUX_URL, token=token, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

class TokenData(BaseModel):
    price : float
    marketcap : float
    liquidity : float

class passToDb(BaseModel):
    token : str
    price : float 


    def price_writer(self):
        point = Point("token_prices").tag("token", self.token).field("price", self.price).time(datetime.now(datetime.timezone.utc()))
        write_api.write(bucket=BUCKET, record=point)
        print(f"Wrote: {self.token} - {self.price:.2f}")

