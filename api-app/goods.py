#   Copyright 2019 NEC Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# coding: utf-8

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from datetime import datetime
import traceback
import os
import json
import math

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

# Round Price
NUM_DIGITS = 2

@app.route('/alive', methods=['GET'])
def alive():
    """Keep Alive

    Returns:
        Response: HTTP Respose
    """
    app.logger.debug("call alive()")

    return jsonify({"result": "200", "time": str(datetime.now())}), 200

@app.route('/goods/<int:goods_id>/<string:cur>', methods=['GET'])
def index_goods_id(goods_id, cur):
    """get goods list with goods_id

    Returns:
        Response: HTTP Respose
    """
    try:
        app.logger.debug("call index_goods()")

        # read goods list file
        with open(os.path.dirname(os.path.abspath(__file__)) + '/data/goodsList.json', 'r', encoding='utf-8') as goods_fp:
            goods = json.load(goods_fp)

        # read currency list file
        with open(os.path.dirname(os.path.abspath(__file__)) + '/data/currency.json', 'r', encoding='utf-8') as currency_fp:
            currencies = json.load(currency_fp)

        # read rate list file
        with open(os.path.dirname(os.path.abspath(__file__)) + '/data/rate.json', encoding='utf-8') as rates_fp:
            rates = json.load(rates_fp)

        # Calculate the price of each currency
        resp_goods = []
        goods_cnt = 0

        for item in goods['goods']:
            resp_price = []
            goods_cnt += 1

            # Get goods list with goods_id
            if goods_id != goods_cnt:
                continue

            # Calculate the price from the rate
            if cur == 'YEN':
                price = item['price']
            else:
                price = math.ceil(item['price'] / rates[cur] * pow(10,NUM_DIGITS)) / pow(10,NUM_DIGITS)

            resp_price.append(
                {
                    'currency' : cur,
                    'symbol' : currencies[cur]['symbol'],
                    'value' : price,
                    'formated_value' : (currencies[cur]['formatter']).format(symbol=currencies[cur]['symbol'], price=price),
                }
            )
            
            resp_goods.append(
                {
                    "id" : goods_cnt,
                    "name" : item['name'],
                    "price" : resp_price,
                }
            )

        return jsonify({"result": "200", "goods": resp_goods, "time": str(datetime.now())}), 200

    except Exception as e:
        app.logger.error(''.join(list(traceback.TracebackException.from_exception(e).format())))
        return jsonify({'result': '500'}), 500

@app.route('/currencies', methods=['GET'])
def index_currencies():
    """Get currencies

    Returns:
        Response: HTTP Respose
    """
    app.logger.debug("call index_currencies()")

    try:
        # read currency list file
        with open(os.path.dirname(os.path.abspath(__file__)) + '/data/currency.json', 'r', encoding='utf-8') as currency_fp:
            currencies = json.load(currency_fp)

        resp_currencies = []
        for key_str in currencies.keys():
            item = {
                "label": key_str,
                "value": key_str,
            }
            resp_currencies.append(item)

        return jsonify({"result": "200", "currencies": resp_currencies, "time": str(datetime.now())}), 200

    except Exception as e:
        app.logger.error(''.join(list(traceback.TracebackException.from_exception(e).format())))
        return jsonify({'result': '500'}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('API_PORT', '8000')), threaded=True)
