#!/usr/bin/python3

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import bluetooth as bl
import ctypes
import os



app = Flask(__name__, static_folder='../client-ctypes-blue', static_url_path='/')
app.config['SECRET_KEY'] = '24sad@57dasda554'

CORS(app, resource = {r'/*': {
    'origins': '*',
    'allow_headers': 'Access-Control-Allow-Origin'
}})

socketio = SocketIO(app, cors_allowed_origins='*')
lib_path = os.path.abspath("./c/StringFunction.so")
lib_c = ctypes.CDLL(lib_path)

def ctypes_data(string):
    if string:
        mutable_string = ctypes.create_string_buffer(str.encode(string))
        lib_c.add_one_to_string(mutable_string)
        return mutable_string
    return ''

class BluetoothServer:

    SIZE = 1
    BACKLOG = 1
    PORT = 1
    DATA_SIZE = 1024

    def __init__(self):
        self.connection = False

    def start(self):
        print('[~] Initialization bluetooth socket')
        self.socket = bl.BluetoothSocket(bl.RFCOMM)
        self.socket.bind(('', self.PORT))
        self.socket.listen(self.BACKLOG)

    def stop(self):
        print('[-] Disconnected Bluetooth Socket')
        self.socket.close()

    def _recv_data(self, client_socket):
        while True:
            try:
                original_string = client_socket.recv(self.DATA_SIZE).decode('utf-8')
                if len(original_string) == 0:
                    break
                print(f"[+] Data from client: {original_string}")

                mutable_string = ctypes_data(original_string)
                json_data = {
                    'original': original_string,
                    'mutable': mutable_string.value.decode('utf-8')
                }
                socketio.emit('blue-data', json_data)
                client_socket.send('OK')
                socketio.sleep(1)
            except bl.BluetoothError:
                print("[-] Disconnected...")
                socketio.emit('blue-data', {'data': 'Client is disconnect!'})
                socketio.sleep(1)
                self.connection = False
                break

    def accept_connection_and_send_data(self):
        while True:
            try:
                print('[?] Trying to connect...')
                client_socket, info_client = self.socket.accept()
                self.connection = True
                socketio.emit('blue-data', {'data': 'Client is connected!'})
                socketio.sleep(1)
                print(f"[*] Accept connection from {info_client}")
                self._recv_data(client_socket)
            except KeyboardInterrupt:
                print('[~] Bey bey!')
                break
            except Exception:
                self.start()
                self.connection = False
                break

    def is_connected(self):
        return self.connection

socketbl = BluetoothServer()


@app.route('/')
def index():
    return app.send_static_file('index.html')

@socketio.on('connect')
def handle_connect(msg):
    print('[*] User is connected!')

@socketio.on('response-data')
def handle_ctype_data(msg):
    if socketbl.is_connected() == False:
        print('[*] Socket start...')
        socketbl.start()
    socketbl.accept_connection_and_send_data()

if __name__ == '__main__':
    app.debug = True
    socketio.run(app, host='192.168.137.111', port=5000)