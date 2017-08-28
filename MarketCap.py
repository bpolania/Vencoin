# import urllib2
# import json
#
# def getTotalMarketCap(coinsArray):
#     totalMarketCap = 0
#     for coin in json.loads(coinsArray):
#         if coin['market_cap_usd'] != None:
#             totalMarketCap += float(coin['market_cap_usd'])
#     return totalMarketCap
#
# def calculateCapitalizationIndexValue(totalMarketCap, coinsArray, indexes):
#     totalMarketCap = 0
#     totalIndexes = 0
#     for i in range(0,indexes):
#         coin = json.loads(coinsArray)[i]
#         if coin['market_cap_usd'] != None:
#             totalIndexes += 1
#             totalMarketCap += float(coin['market_cap_usd'])
#
#     return totalMarketCap*(float(100)/21000000)
#
# def calculateProportionalIndexValue(totalMarketCap, coinsArray, limit):
#     share = 0
#     totalIndexes = 0
#     currentMarketCap = 0
#     for coin in json.loads(coinsArray):
#         if coin['market_cap_usd'] != None:
#             if share < limit:
#                 totalIndexes += 1
#                 share += (float(coin['market_cap_usd']) * 100)/totalMarketCap
#                 currentMarketCap += float(coin['market_cap_usd'])
#     return str(currentMarketCap*(float(100)/21000000))
#
#
#
# def calculateMarketShare(totalMarketCap, coinsArray):
#     for coin in json.loads(coinsArray):
#         if coin['market_cap_usd'] != None:
#             return coin['id'],(float(coin['market_cap_usd']) * 100)/totalMarketCap
#
# coins = urllib2.urlopen("https://api.coinmarketcap.com/v1/ticker/").read()
# totalMarketCap = getTotalMarketCap(coins)
# #print totalMarketCap
# # calculateMarketShare(totalMarketCap, coins)
# print calculateProportionalIndexValue(totalMarketCap, coins, 80)

from flask import Flask
application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Hello, World!'
