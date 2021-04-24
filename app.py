from prometheus_client import start_http_server, Summary, Gauge
import requests
import os
import sys

import logging

import time

logger = logging.getLogger(__name__)

ACCOUNT_ID = os.getenv("ACCOUNT_ID", None)
if ACCOUNT_ID == None:
    logger.error("ACCOUNT_ID must be set to continue")
    sys.exit(1)

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", None)
if ACCESS_TOKEN == None:
    logger.error("ACCESS_TOKEN must be set to continue")
    sys.exit(2)

HTTP_PORT = os.getenv("HTTP_PORT", 9823)
UPDATE_FREQUENCY = os.getenv("UPDATE_FREQUENCY",1800)



if __name__ == "__main__":
    start_http_server(int(HTTP_PORT))

    while True:
        # Update Metrics and snooze
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "accept": "application/json"
        }
        r = requests.get(f"https://api.monzo.com/balance?account_id={ACCOUNT_ID}", headers=headers)
        if r.status_code != 200:
            logger.error(f"API did not return OK {r.text}")
        else:
            data = r.json()
            unit = data["currency"]
            balance = Gauge("monzo_account_balance",f"Current Monzo account balance in {unit}")
            balance.set((float(data["balance"])/100.0))
            total_balance = Gauge("monzo_total_balance", f"Total Monzo balance (combined total of all pots, and current account)")
            total_balance.set((float(data["total_balance"])/100.0))

        time.sleep(int(UPDATE_FREQUENCY))