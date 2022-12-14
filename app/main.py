from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import json
 
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_data():
  file = open('app/data.json')
  return json.load(file)

@app.route('/quantity', methods=['GET'])
def index():
  data = get_data()
  return Response(str({'len': len(data)}), status=200, mimetype='application/json')

@app.route('/missing_money', methods=['GET'])
def missing_money():
  data = get_data()
  missing_money_tables = list(filter(lambda table: sum(product['price'] * product['quantity'] for product in table['products'])
             > sum(paymeny['amount'] for paymeny in table['payments']), data))
  for table in missing_money_tables:
    table['missing_money'] = sum(product['price'] * product['quantity'] for product in table['products'])
    - sum(paymeny['amount'] for paymeny in table['payments'])
    
  return Response(json.dumps(missing_money_tables), status=200, mimetype='application/json')

@app.route('/sells_per_waiter', methods=['GET'])
def sells_per_waiter():
  data = get_data()
  sells = {}
  for table in data:
    if table['waiter'] not in sells:
      sells[table['waiter']] = {'quantity': 1, 'income': table['total']}
    else:
      sells[table['waiter']]['quantity'] += 1
      sells[table['waiter']]['income'] += table['total']

  return Response(json.dumps(sells), status=200, mimetype='application/json')
  
@app.route('/sells_per_cashier', methods=['GET'])
def sells_per_cashier():
  data = get_data()
  sells = {}
  for table in data:
    if table['cashier'] not in sells:
      sells[table['cashier']] = {'quantity': 1, 'income': table['total']}
    else:
      sells[table['cashier']]['quantity'] += 1
      sells[table['cashier']]['income'] += table['total']

  return Response(json.dumps(sells), status=200, mimetype='application/json')

@app.route('/purchases_by_category', methods=['GET'])
def purchases_by_category():
  data = get_data()
  sells = {}
  for table in data:
    for product in table['products']:
      if product['category'] not in sells:
        sells[product['category']] = {'quantity': 1, 'income': product['price']}
      else:
        sells[product['category']]['quantity'] += 1
        sells[product['category']]['income'] += product['price']

  return Response(json.dumps(sells), status=200, mimetype='application/json')

@app.route('/purchases_by_pay_method', methods=['GET'])
def purchases_by_pay_method():
  data = get_data()
  sells = {}
  for table in data:
    for payment in table['payments']:
      if payment['type'] not in sells:
        sells[payment['type']] = payment['amount']
      else:
        sells[payment['type']] += payment['amount']

  return Response(json.dumps(sells), status=200, mimetype='application/json')

@app.route('/purchases_by_zone', methods=['GET'])
def purchases_by_zone():
  data = get_data()
  sells = {}
  for table in data:
    if table['zone'] not in sells:
      sells[table['zone']] = {'quantity': 1, 'income': table['total']}
    else:
      sells[table['zone']]['quantity'] += 1
      sells[table['zone']]['income'] += table['total']

  return Response(json.dumps(sells), status=200, mimetype='application/json')

@app.route('/categories_by_zone', methods=['GET'])
def categories_by_zone():
  data = get_data()
  zones = {}
  for table in data:
    for product in table['products']:
      if table['zone'] not in zones:
        zones[table['zone']] = {product['category']: {'quantity': 1, 'income': product['price']}}
      elif product['category'] not in zones[table['zone']]:
        zones[table['zone']][product['category']] = {'quantity': 1, 'income': product['price']}
      else:
        zones[table['zone']][product['category']]['quantity'] += 1
        zones[table['zone']][product['category']]['income'] += product['price']

  return Response(json.dumps(zones), status=200, mimetype='application/json')

@app.route('/ping', methods=['GET'])
def ping():
  data = get_data()
  return Response('ok', status=200, mimetype='application/json')

if __name__ == '__main__':
   app.run(port=8000, debug=True)