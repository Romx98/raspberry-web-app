from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__, )
CORS(app, resources = {r'/*': {
    'origins': '*',
    'allow_headers': 'Access-Control-Allow-Origin'
}})





if __name__ == '__main__':
    app.run()