from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from .services.bluetooth_service import BluetoothServer

app = Flask(__name__, static_folder='../client-blue/dist/', static_url_path='/')


CORS(app, resources = {r'/*': {
    'origins': '*',
    'allow_headers': 'Access-Control-Allow-Origin'
}})

socketio = SocketIO(app, cors_allowed_origins='*')
blue_sock = BluetoothServer()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@socketio.on('connect')
def handle_message():
    print("VOLA SA \"handle_message\"")
    emit('MESSAGE', {'data': blue_sock.recv()})

if __name__ == '__main__':
    socketio.run(app, host='192.168.137.111', port=8000)