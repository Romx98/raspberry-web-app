from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from .services.serverServices import ConstantString, ServerUtils, BluetoothServer


app = Flask(__name__, static_folder='../client-blue/dist/', static_url_path='/')

CORS(app, resources = {r'/*': {
    'origins': '*',
    'allow_headers': 'Access-Control-Allow-Origin'
}})

socket_io = SocketIO(app, cors_allowed_origins='*')
socket_bl = BluetoothServer(socket_io)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@socket_io.on('connect')
def handle_connect(json):
    ServerUtils.emit_to_client(socket_io, ConstantString.SERVER_OPENED)

@socket_io.on('disconnect')
def handle_disconnect():
    socket_bl.stop_socket()
    ServerUtils.emit_to_client(socket_io, ConstantString.SERVER_CLOSED)


@socket_io.on('response-data')
def handle_bluetooth_data(json):
    if socket_bl.is_connected() == False:
        print('[*] Socket start...')
        socket_bl.start_socket_bl()
    socket_bl.accept_connection_and_send_data()


if __name__ == '__main__':
    socket_io.run(app, host='192.168.137.111', port=5000)
