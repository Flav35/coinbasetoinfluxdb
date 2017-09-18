#!/usr/bin/env python3
import os
from coinbase.wallet.client import Client as cb_client
import influxdb
import time

class CoinBase:
    def __init__(self, api_key, api_secret_key):
        self.api_key = api_key
        self.api_private = api_secret_key
        self.client = cb_client(self.api_key, self.api_private)

    def get_currentmoney(self):
        accounts = self.client.get_accounts()['data']
        currency = []
        for i in accounts:
            currency.append({ 'currency': i['native_balance']['currency'], 'amount': i['native_balance']['amount'], 'crypto_money': i['balance']['currency'], 'date': i['created_at']})
        return currency

class InfluxdbManagement:
    def __init__(self, host, port, db_name):
        self.host = host
        self.port = port
        self.db = db_name
        self.client = influxdb.InfluxDBClient(host=self.host, port=self.port, database=self.db)

    def manage_db(self):
        try:
            self.client.create_database(self.db)
        except Exception as e: 
            print(e)

    def push_data(self, data):
        payload = [{
                'measurement': 'crypto_' + data['currency'],
                'tags': [],
                'times': data['date'],
                'fields': {
                    'currency': data['currency'],
                    'amount': float(data['amount']),
                    'crypto_money': data['crypto_money']}
                }]
        try:
            self.client.write_points(payload)
        except Exception as e:
            print(e)
        print(payload)

if __name__ == "__main__":
    API_KEY = os.getenv('COINBASE_API_KEY')
    API_PRIVATE = os.getenv('COINBASE_API_SECRET_KEY')
    INFLUX_HOST = os.getenv('INFLUXDB_HOST')
    INFLUX_PORT = 8086
    INFLUX_DB = "coinbase"
    db_connect = InfluxdbManagement(INFLUX_HOST, INFLUX_PORT, INFLUX_DB)
    db_connect.manage_db()
    client = CoinBase(API_KEY, API_PRIVATE)
    while True:
        for i in client.get_currentmoney():
            db_connect.push_data(i)
            time.sleep(30)
