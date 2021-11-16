from flask import Flask, jsonify
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


class BluetoothServer:

    SIZE = 1
    BACKLOG = 1
    PORT = 1
    DATA_SIZE = 1024

    def __init__(self):
        self.socket = bl.BluetoothSocket(bl.RFCOMM)

    def start(self):
        self.socket.bind(('', self.PORT))
        self.socket.listen(self.BACKLOG)
        
    def stop(self):
        print('[-] Disconnected Bluetooth Socket')
        self.socket.close()

    def _recv_data(self, client_socket):
        while True:
            try:
                data = client_socket.recv(self.DATA_SIZE).decode('utf-8')
                print(f"[+] Data from client: {data}")
                client_socket.send('OK')
                socketio.emit('blue-data', {'data': data})
            except bl.BluetoothError:
                print("[-] Disconnected...")
                break


    def accept_connection_and_send_data(self):
        while True:
            try:
                print('[?] Trying to connect...')
                client_socket, info_client = self.socket.accept()
                print(f"[*] Accept connection from {info_client}")

                self._recv_data(client_socket)
            except Exception as e:
                print(e)
                break

blue_sock = BluetoothServer()
blue_sock.start()


@app.route('/')
def index():
    return app.send_static_file('index.html')

@socketio.on('bluetooth data')
def handle_bluetooth_data():
    blue_sock.accept_connection_and_send_data()

if __name__ == '__main__':
    socketio.run(app, host='192.168.137.111', port=8000)