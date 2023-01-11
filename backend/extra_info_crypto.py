import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import datetime
import requests

# load dotEnv
load_dotenv()

# ct stores current time
ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
today = datetime.datetime.now() - datetime.timedelta(days=1)
today = today.strftime("%Y-%m-%d")
# print(today)

# DEFINE GLOBAL VARS
symbols = []
crypto_dict = {}
cg_coins = []

# crypoLabels = ["coingecko_id", "symbol", "name", "asset_platform_id", "block_time_in_minutes", "hashing_algorithm", "categories", "description", "homepage_url", "thumb_url", "small_url", "large_url", "country_origin", "genesis_date", "sentiment_votes_up_percentage", "sentiment_votes_down_percentage", "market_cap_rank", "coingecko_rank", "coingecko_score", "developer_score", "community_score", "liquidity_score", "public_interest_score", "alltime_high", "alltime_high_date", "alltime_low", "alltime_low_date", "market_cap", "fully_diluted_valuation", "total_volume", "high_24h", "low_24h", "price_change_24h", "price_change_percentage_1h", "price_change_percentage_24h", "price_change_percentage_7d", "price_change_percentage_14d", "price_change_percentage_30d", "price_change_percentage_60d", "price_change_percentage_200d", "price_change_percentage_1y", "market_cap_change_24h", "market_cap_change_percentage_24h", "total_supply", "max_supply", "circulating_supply", "alexa_rank", "last_updated"]

# Connect to PlanetScale DB
connection = mysql.connector.connect(
host=os.getenv("HOST"),
database=os.getenv("DATABASE"),
user=os.getenv("DB_USER"),
password=os.getenv("PASSWORD"),
ssl_ca=os.getenv("SSL_CERT")
)
try:
    if connection.is_connected():
        cursor = connection.cursor(dictionary=True)
except Error as e:
    print("Error while connecting to MySQL", e)


# DB FUNCTIONS - get all symbols
sql = "SELECT DISTINCT id, symbol from crypto_trade ORDER BY symbol ASC"
cursor.execute(sql)
records = cursor.fetchall()
for row in records:
    symbol = row['symbol']
    symbolSplit = symbol.split('/')
    for splitted in symbolSplit:
        # print(splitted)
        if splitted != 'USD':
            symbols.append(splitted.lower())
symbols = sorted(set(symbols))

def insertCoinData(coingecko_id, symbol, name, asset_platform_id, block_time_in_minutes, hashing_algorithm, categories, description, homepage_url, thumb_url, small_url, large_url, country_origin, genesis_date, sentiment_votes_up_percentage, sentiment_votes_down_percentage, market_cap_rank, coingecko_rank, coingecko_score, developer_score, community_score, liquidity_score, public_interest_score, alltime_high, alltime_high_date, alltime_low, alltime_low_date, market_cap, fully_diluted_valuation, total_volume, high_24h, low_24h, price_change_24h, price_change_percentage_1h, price_change_percentage_24h, price_change_percentage_7d, price_change_percentage_14d, price_change_percentage_30d, price_change_percentage_60d, price_change_percentage_200d, price_change_percentage_1y, market_cap_change_24h, market_cap_change_percentage_24h, total_supply, max_supply, circulating_supply, alexa_rank, last_updated):
    insert_stmt = "INSERT IGNORE INTO crypto_coin (coingecko_id, symbol, name, asset_platform_id, block_time_in_minutes, hashing_algorithm, categories, description, homepage_url, thumb_url, small_url, large_url, country_origin, genesis_date, sentiment_votes_up_percentage, sentiment_votes_down_percentage, market_cap_rank, coingecko_rank, coingecko_score, developer_score, community_score, liquidity_score, public_interest_score, alltime_high, alltime_high_date, alltime_low, alltime_low_date, market_cap, fully_diluted_valuation, total_volume, high_24h, low_24h, price_change_24h, price_change_percentage_1h, price_change_percentage_24h, price_change_percentage_7d, price_change_percentage_14d, price_change_percentage_30d, price_change_percentage_60d, price_change_percentage_200d, price_change_percentage_1y, market_cap_change_24h, market_cap_change_percentage_24h, total_supply, max_supply, circulating_supply, alexa_rank, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    data = (coingecko_id, symbol, name, asset_platform_id, block_time_in_minutes, hashing_algorithm, categories, description, homepage_url, thumb_url, small_url, large_url, country_origin, genesis_date, sentiment_votes_up_percentage, sentiment_votes_down_percentage, market_cap_rank, coingecko_rank, coingecko_score, developer_score, community_score, liquidity_score, public_interest_score, alltime_high, alltime_high_date, alltime_low, alltime_low_date, market_cap, fully_diluted_valuation, total_volume, high_24h, low_24h, price_change_24h, price_change_percentage_1h, price_change_percentage_24h, price_change_percentage_7d, price_change_percentage_14d, price_change_percentage_30d, price_change_percentage_60d, price_change_percentage_200d, price_change_percentage_1y, market_cap_change_24h, market_cap_change_percentage_24h, total_supply, max_supply, circulating_supply, alexa_rank, last_updated)
    cursor.execute(insert_stmt, data)
    connection.commit()

# Get CoinGecko ID for coins that are Oanda tradable pairs
cg_coins_url = os.getenv("CG_COINS_URL") 
cg_coins_list_url = str(cg_coins_url) + "/list"
response = requests.get(url = cg_coins_list_url)
oandaAsset = response.json()
# print(oandaAsset[0])
for asset in oandaAsset:
    # print(asset)
    for key in asset:
        # print("Symbol: ", asset["symbol"])
        if asset[key] in symbols:
            cg_coins.append(asset["symbol"])
            crypto_dict[asset["symbol"]] = asset["id"]
crypto_dict["eth"] = 'ethereum'
cg_coins = sorted(set(cg_coins))
# print(crypto_dict)


# Connect to Oanda API
def getCryptoInfo(symbol):
    params = {
        "localization":"false",
        "tickers":"false",
        "market_data":"true",
        "community_data":"false",
        "developer_data":"false",
        "sparkline":"false",
    }
    cg_id = crypto_dict[symbol]
    cg_id = 'ethereum' if symbol == 'eth' else cg_id
    cg_id = 'chainlink' if symbol == 'link' else cg_id
    print(cg_id)
    cg_coin_data_url = str(cg_coins_url) + "/" + cg_id
    response = requests.get(url = cg_coin_data_url)
    coinAsset = response.json()
    for key in coinAsset:
        # coinData[key] = coinAsset[key]# print(coinAsset["market_data"]["total_supply"])
        # print (coinAsset["name"])
        
        categories = ''
        homepage = ''
        fully_diluted_valuation = ''
        high_24h = 0
        
        if coinAsset["categories"]:
            for category in coinAsset["categories"]:
                categories += category + ";"
            categories = categories.rstrip(';')
        
        if len(coinAsset["links"]["homepage"]) > 1:
            homepage = coinAsset["links"]["homepage"][0]
        
        if coinAsset["market_data"]["fully_diluted_valuation"]:
            fully_diluted_valuation = coinAsset["market_data"]["fully_diluted_valuation"]["usd"]
        
        if coinAsset["market_data"]["high_24h"]:
            try:
                if coinAsset["market_data"]["high_24h"]["usd"]:
                    high_24h = coinAsset["market_data"]["high_24h"]["usd"]
                elif high_24h == 0 and coinAsset["market_data"]["high_24h"]["USD"]:
                    high_24h = coinAsset["market_data"]["high_24h"]["USD"]
            except Error as e:
                print("Error while connecting to MySQL", e)
                
        
        coingecko_id = cg_id
        symbol = coinAsset["symbol"]
        name = coinAsset["name"]
        asset_platform_id = coinAsset["asset_platform_id"]
        block_time_in_minutes = coinAsset["block_time_in_minutes"]
        hashing_algorithm = coinAsset["hashing_algorithm"]
        categories = categories
        description = coinAsset["description"]["en"]
        homepage_url = homepage
        thumb_url = coinAsset["image"]["thumb"]
        small_url = coinAsset["image"]["small"]
        large_url = coinAsset["image"]["large"]
        country_origin = coinAsset["country_origin"]
        genesis_date = coinAsset["genesis_date"]
        sentiment_votes_up_percentage = coinAsset["sentiment_votes_up_percentage"]
        sentiment_votes_down_percentage = coinAsset["sentiment_votes_down_percentage"]
        market_cap_rank = coinAsset["market_cap_rank"]
        coingecko_rank = coinAsset["coingecko_rank"]
        coingecko_score = coinAsset["coingecko_score"]
        developer_score = coinAsset["developer_score"]
        community_score = coinAsset["community_score"]
        liquidity_score = coinAsset["liquidity_score"]
        public_interest_score = coinAsset["public_interest_score"]
        alltime_high = coinAsset["market_data"]["ath"]["usd"]
        alltime_high_date = coinAsset["market_data"]["ath_date"]["usd"]
        alltime_low = coinAsset["market_data"]["atl"]["usd"]
        alltime_low_date = coinAsset["market_data"]["atl_date"]["usd"]
        market_cap = coinAsset["market_data"]["market_cap"]["usd"]
        fully_diluted_valuation = fully_diluted_valuation
        total_volume = coinAsset["market_data"]["total_volume"]["usd"]
        high_24h = high_24h
        low_24h = coinAsset["market_data"]["low_24h"]["usd"]
        price_change_24h = coinAsset["market_data"]["price_change_24h_in_currency"]["usd"]
        price_change_percentage_1h = coinAsset["market_data"]["price_change_percentage_1h_in_currency"]["usd"]
        price_change_percentage_24h = coinAsset["market_data"]["price_change_percentage_24h_in_currency"]["usd"]
        price_change_percentage_7d = coinAsset["market_data"]["price_change_percentage_7d_in_currency"]["usd"]
        price_change_percentage_14d = coinAsset["market_data"]["price_change_percentage_14d_in_currency"]["usd"]
        price_change_percentage_30d = coinAsset["market_data"]["price_change_percentage_30d_in_currency"]["usd"]
        price_change_percentage_60d = coinAsset["market_data"]["price_change_percentage_60d_in_currency"]["usd"]
        price_change_percentage_200d = coinAsset["market_data"]["price_change_percentage_200d_in_currency"]["usd"]
        price_change_percentage_1y = coinAsset["market_data"]["price_change_percentage_1y_in_currency"]["usd"]
        market_cap_change_24h = coinAsset["market_data"]["market_cap_change_24h_in_currency"]["usd"]
        market_cap_change_percentage_24h = coinAsset["market_data"]["market_cap_change_percentage_24h_in_currency"]["usd"]
        total_supply = coinAsset["market_data"]["total_supply"]
        max_supply = coinAsset["market_data"]["max_supply"]
        circulating_supply = coinAsset["market_data"]["circulating_supply"]
        alexa_rank = coinAsset["public_interest_stats"]["alexa_rank"]
        last_updated = coinAsset["last_updated"]
        
        insertCoinData(coingecko_id, symbol, name, asset_platform_id, block_time_in_minutes, hashing_algorithm, categories, description, homepage_url, thumb_url, small_url, large_url, country_origin, genesis_date, sentiment_votes_up_percentage, sentiment_votes_down_percentage, market_cap_rank, coingecko_rank, coingecko_score, developer_score, community_score, liquidity_score, public_interest_score, alltime_high, alltime_high_date, alltime_low, alltime_low_date, market_cap, fully_diluted_valuation, total_volume, high_24h, low_24h, price_change_24h, price_change_percentage_1h, price_change_percentage_24h, price_change_percentage_7d, price_change_percentage_14d, price_change_percentage_30d, price_change_percentage_60d, price_change_percentage_200d, price_change_percentage_1y, market_cap_change_24h, market_cap_change_percentage_24h, total_supply, max_supply, circulating_supply, alexa_rank, last_updated)
    
    print(str(ct)+": " + symbol + " details updated! (i.e. " + coingecko_id + ")")

    # print(type(coingecko_id), type(symbol), type(name), type(asset_platform_id), type(block_time_in_minutes), type(hashing_algorithm), type(categories), type(description), type(homepage_url), type(thumb_url), type(small_url), type(large_url), type(country_origin), type(genesis_date), type(sentiment_votes_up_percentage), type(sentiment_votes_down_percentage), type(market_cap_rank), type(coingecko_rank), type(coingecko_score), type(developer_score), type(community_score), type(liquidity_score), type(public_interest_score), type(alltime_high), type(alltime_high_date), type(alltime_low), type(alltime_low_date), type(market_cap), type(fully_diluted_valuation), type(total_volume), type(high_24h), type(low_24h), type(price_change_24h), type(price_change_percentage_1h), type(price_change_percentage_24h), type(price_change_percentage_7d), type(price_change_percentage_14d), type(price_change_percentage_30d), type(price_change_percentage_60d), type(price_change_percentage_200d), type(price_change_percentage_1y), type(market_cap_change_24h), type(market_cap_change_percentage_24h), type(total_supply), type(max_supply), type(circulating_supply), type(alexa_rank), type(last_updated))

# Fetch coin data from CG coins that exist in Oanda coins
# print(symbols)
# print(cg_coins)
for symbol in symbols:
    # print(symbol)
    
    if symbol in cg_coins:
        print("-----")
        print(symbol)
        getCryptoInfo(symbol)