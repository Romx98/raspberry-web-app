from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import bluetooth as bl

app = Flask(__name__, static_folder='../client-blue/dist/', static_url_path='/')


CORS(app, resources = {r'/*': {
    'origins': '*',
    'allow_headers': 'Access-Control-Allow-Origin'
}})


class BluetoothServer:

    SIZE = 1
    BACKLOG = 1
    PORT = 1
    DATA_SIZE = 1024

    def __init__(self):
        #self.socket = bl.BluetoothSocket(bl.RFCOMM)
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
                data = client_socket.recv(self.DATA_SIZE).decode('utf-8')
                if len(data) == 0:
                    break
                print(f"[+] Data from client: {data}")
                socketio.emit('blue data', {'data': data})
                client_socket.send('OK')
                socketio.sleep(1)
            except bl.BluetoothError:
                print("[-] Disconnected...")
                socketio.emit('blue data', {'data': 'Client is disconnect!'})
                socketio.sleep(1)
                self.connection = False
                break

    def accept_connection_and_send_data(self):
        while True:
            try:
                print('[?] Trying to connect...')
                client_socket, info_client = self.socket.accept()
                self.connection = True
                socketio.emit('blue data', {'data': 'Client is connected!'})
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


socketio = SocketIO(app, cors_allowed_origins='*')
socketbl = BluetoothServer()


@app.route('/')
def index():
    return app.send_static_file('index.html')

@socketio.on('connect')
def handle_connect(json):
    socketio.emit('blue data', {'data': 'Server is opened!'})

@socketio.on('disconnect')
def handle_disconnect():
    socketbl.stop()
    socketio.emit('blue data', {'data': 'Server is closed!'})

@socketio.on('my event')
def handle_bluetooth_data(json):
    if socketbl.is_connected() == False:
        print('[*] Socket start...')
        socketbl.start()
    socketbl.accept_connection_and_send_data()


if __name__ == '__main__':
    socketio.run(app, host='192.168.137.111', port=5000)
