from flask import Flask, jsonify
from flask_cors import CORS
from .services.bluetooth_service import BluetoothServer

app = Flask(__name__, static_folder='../client-blue/dist/', static_url_path='/')
blue_sock = BluetoothServer()
blue_sock.start()

CORS(app, resources = {r'/*': {
    'origins': '*',
    'allow_headers': 'Access-Control-Allow-Origin'
}})


@app.route('/message')
def get_message():
    if blue_sock.is_connected() == True:
        return jsonify({'msg': blue_sock.recv()})
    elif blue_sock.is_connected() == False or blue_sock.is_connected() == None:
        return jsonify({'msg': 'Disconnect...'})


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run()