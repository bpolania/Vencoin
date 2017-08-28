from flask import g, Flask
from flask import render_template
from flask import request
from sqlite3 import dbapi2 as sqlite3

import plotly.plotly as py
from plotly.graph_objs import *

import urllib2
import json
import threading
import time
import random
import os
import datetime

application = Flask(__name__)
application.config.update(dict(
        DATABASE=os.path.join(application.root_path, 'test.db'),
    ))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(application.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Initializes the database."""
    db = get_db()
    with application.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def getTotalMarketCap(coinsArray):
    totalMarketCap = 0
    for coin in json.loads(coinsArray):
        if coin['market_cap_usd'] != None:
            totalMarketCap += float(coin['market_cap_usd'])
    return totalMarketCap

def calculateCapitalizationIndexValue(totalMarketCap, coinsArray, indexes):
    totalMarketCap = 0
    totalIndexes = 0
    includedCoins = []
    for i in range(0,indexes):
        coin = json.loads(coinsArray)[i]
        if coin['market_cap_usd'] != None:
            totalIndexes += 1
            includedCoins.append(coin['name'])
            totalMarketCap += float(coin['market_cap_usd'])
    return str(round(totalMarketCap*(float(100)/21000000),2)), includedCoins

def calculateProportionalIndexValue(totalMarketCap, coinsArray, limit):
    share = 0
    totalIndexes = 0
    currentMarketCap = 0
    includedCoins = []
    for coin in json.loads(coinsArray):
        if coin['market_cap_usd'] != None:
            if share < limit:
                totalIndexes += 1
                includedCoins.append(coin['name'])
                share += (float(coin['market_cap_usd']) * 100)/totalMarketCap
                currentMarketCap += float(coin['market_cap_usd'])
    return str(round(currentMarketCap*(float(100)/21000000),2)), includedCoins

def calculateMarketShare(totalMarketCap, coinsArray):
    for coin in json.loads(coinsArray):
        if coin['market_cap_usd'] != None:
            return coin['id'],(float(coin['market_cap_usd']) * 100)/totalMarket

def updateParetoIndex(proportional):
    with application.app_context():
        print "pareto record made"
        db = get_db()
        command = "INSERT INTO pareto (value) VALUES (%s)" % proportional
        print command
        cur = db.execute(command)
        db.commit()

def updateTopIndex(capitalization):
    with application.app_context():
        print "top record made"
        db = get_db()
        command = "INSERT INTO top (value) VALUES (%s)" % capitalization
        print command
        cur = db.execute(command)
        db.commit()

def isMobilePlatform():
    platform = request.user_agent.platform
    if platform != None:
        if platform == 'android' or platform == 'iphone':
            return True
        else:
            return False
    return False

py.sign_in("bpolania","0zj1TFWX7ILKbk8jmU3C")
#py.sign_in(os.environ['PLOTLY_USERNAME'],os.environ['PLOTLY_API_KEY'])
coins = ""
proportional = ""
capitalization = ""
proportionalCoins = []
capitalizationCoins = []
def indexDaemon():
    while True:
        global coins
        coins = urllib2.urlopen("https://api.coinmarketcap.com/v1/ticker/").read()
        totalMarketCap = getTotalMarketCap(coins)
        proportional, proportionalCoins = calculateProportionalIndexValue(totalMarketCap, coins, 80)
        capitalization, capitalizationCoins = calculateCapitalizationIndexValue(totalMarketCap, coins, 500)
        updateParetoIndex(proportional)
        updateTopIndex(capitalization)
        #print coins
        time.sleep(300)

thread = threading.Thread(name='indexDaemon', target=indexDaemon)
thread.setDaemon(True)
thread.start()

@application.route('/')
def hello_world():
    totalMarketCap = getTotalMarketCap(coins)
    proportional, proportionalCoins = calculateProportionalIndexValue(totalMarketCap, coins, 80)
    capitalization, capitalizationCoins = calculateCapitalizationIndexValue(totalMarketCap, coins, 500)
    return render_template('index.html', proportional=proportional, capitalization=capitalization)

# @application.route('/initdb')
# def initDB():
#     init_db()
#     return "success"

@application.route('/paretoPlot')
def getParetoData():
    db = get_db()
    cur = db.execute('select * from pareto')
    entries = cur.fetchall()
    xData = []
    yData = []
    for entry in entries:
        xData.append(datetime.datetime.fromtimestamp(int(entry[1])).strftime('%Y-%m-%d %H:%M:%S'))
        yData.append(entry[2])
    trace0 = Scatter(x=xData,y=yData)
    data = Data([trace0])
    link = py.plot(data, filename = 'basic-line', fileopt = 'overwrite', auto_open = False)
    isMobile = isMobilePlatform()
    if isMobile == True:
        link.replace("https:", "") + ".jpg"
    else:
        link = link.replace("https:", "") + ".embed?link=false"
    return render_template('pareto_plot.html',link=link, includedCoins = proportionalCoins)

@application.route('/topPlot')
def getTopData():
    db = get_db()
    cur = db.execute('select * from top')
    entries = cur.fetchall()
    xData = []
    yData = []
    for entry in entries:
        xData.append(datetime.datetime.fromtimestamp(int(entry[1])).strftime('%Y-%m-%d %H:%M:%S'))
        yData.append(entry[2])
    trace0 = Scatter(x=xData,y=yData)
    data = Data([trace0])
    link = py.plot(data, filename = 'basic-line', fileopt = 'overwrite', auto_open = False)
    isMobile = isMobilePlatform()
    if isMobile == True:
        link.replace("https:", "") + ".jpg"
    else:
        link = link.replace("https:", "") + ".embed?link=false"
    return render_template('top_plot.html',link=link, includedCoins = capitalization)
