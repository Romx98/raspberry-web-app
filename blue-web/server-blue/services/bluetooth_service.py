
import bluetooth as bl

class BluetoothServer:

    DATA_SIZE = 1024
    BACKLOG = 1
    PORT = 1

    def __init__(self):
        self.client = {}
        self.connected = False

    def start(self):
        self.socket = bl.BluetoothSocket(bl.RFCOMM)
        self.socket.bind(('', self.PORT))
        self.socket.listen(self.BACKLOG)
        self.port = self.socket.getsockname()[1]

        print('[?] Trying to connect...')
        self.client['socket'], self.client['mac_addr'] = self.socket.accept()
        print(f"[*] Accept connection from {self.client['mac_addr']}")
        self.connected = True

    def stop(self):
        print("[-] Disconnected...")
        self.socket.close()
        try:
            self.client['socket'].close()
        except AttributeError:
            pass


    def recv(self):
        try:
            data = self.client['socket'].recv(self.DATA_SIZE).decode('utf-8')
            print(f"[+] Data from client: {data}")
            self.client['socket'].send('OK')
            return data
        except bl.BluetoothError:
            self.stop()
            self.connected = False
            self.start()
            return("Waiting for data...")
        except KeyError:
            self.start()
            return("Waiting for client...")
           

            
