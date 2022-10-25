from flask import Flask, request, Response
import json
 
app = Flask(__name__)

def get_data():
  file = open('data.json')
  return json.load(file)

@app.route('/quantity', methods=['GET'])
def index():
  data = get_data()
  return Response(str({'len': len(data)}), status=200, mimetype='application/json')



if __name__ == '__main__':
   app.run(port=8000, debug=True)