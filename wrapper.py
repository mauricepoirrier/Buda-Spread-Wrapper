import requests
import sys


class BudaWrapper:

    def __init__(self):
        self.url = 'https://www.buda.com/api/v2/'

    def _requestHandler(self,market=None):
        if market == None:
            response = requests.get(self.url+'markets')
        else:
            response = requests.get(self.url+'markets/{}/ticker'.format(market))
        return response.json()
    def _specificSpread(self,market):
        response = self._requestHandler(market)
        min_ask = float(response['ticker']['min_ask'][0])
        max_bid = float(response['ticker']['max_bid'][0])
        return round(min_ask - max_bid,3)

    def spread(self,specificMarket=None):
        if specificMarket == None:
            print("Calculating spread of all markets")
            response = self._requestHandler()
            spreads = {}
            for market in response['markets']:
                spreads[market['id']] = self._specificSpread(market['id'])
            return {'spreads':spreads}
        else:
            print("Calculating spread of {}".format(specificMarket))
            return {specificMarket: self._specificSpread(specificMarket)}

if '__main__' == __name__:
    print("Welcome to Buda Spread Wrapper")
    wrapper = BudaWrapper()
    if len(sys.argv) == 1:
        print(wrapper.spread())
    elif len(sys.argv) == 2:
        print(wrapper.spread(sys.argv[1]))
    else:
        print("Wrong execution, please execute python wrapper.py or python wrapper.py [Market]")
    