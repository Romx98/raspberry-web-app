from datetime import time
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
#from .services.bluetooth_service import BluetoothServer
import bluetooth as bl

app = Flask(__name__, static_folder='../client-blue/dist/', static_url_path='/')


CORS(app, resources = {r'/*': {
    'origins': '*',
    'allow_headers': 'Access-Control-Allow-Origin'
}})


socketio = SocketIO(app, cors_allowed_origins='*')
socket = bl.BluetoothSocket(bl.RFCOMM)
connected = False

def start_bluetooth(socket):
    print('[*] Initialize socket')
    socket.bind(('', 5))
    socket.listen(1)

def stop_blutooth(socket):
    print('[-] Disconnected Bluetooth Socket')
    socket.close()

def _recv_data(client_socket):
    global connected
    while True:
        try:
            data = client_socket.recv(64).decode('utf-8')
            connected = True
            print(f"[+] Data from client: {data}")
            emit('blue data', {'data': data})
            client_socket.send('OK')
        except bl.BluetoothError:
            connected = False
            print("[-] Disconnected...")
            break


def accept_connection_and_send_data():
    print()
    while True:
        try:
            print('[?] Trying to connect...')
            client_socket, info_client = socket.accept()
            print(f"[*] Accept connection from {info_client}")
            _recv_data(client_socket)
        except Exception as e:
            print(e)
            break

start_bluetooth(socket)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@socketio.on('my event')
def handle_bluetooth_data(json):
    while True:
        socketio.emit('blue data', {'data': 'Waiting for connection...'})
        #if connected == False:
        #    accept_connection_and_send_data()
    

if __name__ == '__main__':
    socketio.run(app, port=5000)