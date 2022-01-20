from log1 import setup
import time
import sqlite3
import requests

logger = setup.setup_logging()


def run():
    try:
        endpoint = " https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        body = {
            "page": 1,
            "rows": 10,
            "payTypes": [],
            "asset": "USDT",
            "tradeType": "BUY",
            "fiat": "VND",
            "publisherType": "merchant"
        }
        # Dinh dang data
        headers = {
            "Content-Type": "application/json"
        }
    except Exception as e:

        return f'{logger.error("Error")}'
    try:

        repose = requests.post(url=endpoint, headers=headers, json=body)

        content = repose.json()['data']
        with sqlite3.connect('price.db') as conn:
            curs = conn.cursor()
            curs.execute("CREATE TABLE IF NOT EXISTS price (Price REAL)")
            logger.info("CREATE TABLE")
            for each in content:
                price = float(each['adv']['price'])
                curs.execute("INSERT INTO price VALUES (?)", (price,))
                logger.info("INSERT DATA TO DATABASE")
            print(price)

    except Exception as e:
        logger.exception("Exception:")
        logger.error(e)


def splite():

    try:
        conn = sqlite3.connect("price.db")
        cur = conn.cursor()
        cur.execute("SELECT AVG(price) FROM price")
        rows = cur.fetchall()
        for row in rows:
            logger.warning(row)
    except Exception as e:
        return logger.error(e)


if __name__ == '__main__':
    print("Running!")
    logger.info("----------")
    run()
    splite()

