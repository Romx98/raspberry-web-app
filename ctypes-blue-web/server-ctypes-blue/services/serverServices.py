
import bluetooth as bl


# Class contains only STRINGS
class ConstantString:

    SERVER_OPENED = 'Server is opened!'
    SERVER_CLOSED = 'Server is closed!'
    CLIENT_CONNECTED = 'Client is connected!'
    CLIENT_DISCONNECTED = 'Client is disconnected!'
    SOCKET_EVENT_NAME = 'blue-data'
    SUCCESS_RECV = 'OK'


# Class contains helpfull methods
class ServerUtils:

    def _generate_json(self, original, mutable):
        return {
            'original': original,
            'mutable': mutable
        }

    def _add_one_to_char(self):
        return ''

    def emit_to_client(self, socket_io, original):
        mutable = self._add_one_to_char()
        json_data = self._generate_json(original, mutable)
        socket_io.emit(ConstantString.SOCKET_EVENT_NAME, json_data)
        socket_io.sleep(1)


# Class contians only Bluetooth Socket
class BluetoothServer:

    # Constant
    BACKLOG = 1
    PORT = 1
    DATA_SIZE = 1024

    def __init__(self, socket_io):
        self.socket_io = socket_io
        self.socket_bl = None
        self.connection = False

    def start_socket_bl(self):
        print('[~] Initialization bluetooth socket')
        self.socket_bl = bl.BluetoothSocket(bl.RFCOMM)
        self.socket_bl.bind(('', self.PORT))
        self.socket_bl.listen(self.BACKLOG)

    def stop_socket(self, client_socket):
        try:
            self.client_close(client_socket)
            self.socket_bl.close()
            print('[-] Disconnected Bluetooth Socket')
        except Exception as e:
            print(f'[!!] Can\'t closed! {e}')
        
    def client_close(self, client_socket):
        try:
            client_socket.close()
            self.connection = False
            print("[-] Disconnected client...")
        except Exception as e:
            print(f'[!!] Can\'t disconnected \'client\'! {e}')

    def _recv_from_client(self, socket_client):
        while True:
            try:
                blue_data = socket_client.recv(self.DATA_SIZE).decode('utf-8')
                print(f"[+] Data from client: {blue_data}")
                ServerUtils.emit_to_client(self.socket_io, blue_data)
                socket_client.send(ConstantString.SUCCESS_RECV)
            except bl.BluetoothError:
                self.client_close(socket_client)
                break

    def accept_connection_and_emit(self):
        while True:
            try:
                print('[?] Trying to connect...')
                socket_client, info_client = self.socket_bl.accept()
                ServerUtils.emit_to_client(self.socket_io, ConstantString.CLIENT_CONNECTED)
                print(f"[*] Accept connection from {info_client}")
                self.connection = True
                self._recv_from_client(socket_client)
            except KeyboardInterrupt:
                print('[~] Goodbye!')
                break
            except Exception as e:
                print(f'[!!] Can\'t accept connection! {e}')
                break

    def is_connected(self):
        return self.connection