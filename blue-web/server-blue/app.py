from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from .services.bluetooth_service import BluetoothServer

app = Flask(__name__, static_folder='../client-blue/dist/', static_url_path='/')
socketio = SocketIO(app)
blue_sock = BluetoothServer()

CORS(app, resources = {r'/*': {
    'origins': '*',
    'allow_headers': 'Access-Control-Allow-Origin'
}})


@app.route('/')
def index():
    return app.send_static_file('index.html')


@socketio.on('message')
def handle_message():
    emit('MESSAGE', {'msg': blue_sock.recv()})


if __name__ == '__main__':
    socketio.run(app, port=2345)