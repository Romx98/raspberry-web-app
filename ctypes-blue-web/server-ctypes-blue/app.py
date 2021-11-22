 
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from services.serverServices import *


app = Flask(__name__, static_folder='../client-blue/dist/', static_url_path='/')

CORS(app, resources = {r'/*': {
    'origins': '*',
    'allow_headers': 'Access-Control-Allow-Origin'
}})

socket_io = SocketIO(app, cors_allowed_origins='*')
server_utils = ServerUtils(socket_io)
socket_bl = BluetoothServer(server_utils)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@socket_io.on('connect')
def handle_connect():
    server_utils.emit_to_client(ConstantString.SERVER_OPENED)

@socket_io.on('disconnect')
def handle_disconnect():
    socket_bl.stop_socket()
    server_utils.emit_to_client(ConstantString.SERVER_CLOSED)

@socket_io.on('response-data')
def handle_bluetooth_data(json):
    if socket_bl.is_connected() == False:
        print('[*] Socket start...')
        socket_bl.start_socket_bl()
    socket_bl.accept_connection_and_send_data()

if __name__ == '__main__':
    host = '192.168.137.111'
    socket_io.run(app, port=5000)
