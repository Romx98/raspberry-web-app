
import bluetooth as bl

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

    

if __name__ == '__main__':
    blue = BluetoothServer()
    blue.start()
    blue.accept_connection_and_send_data()
    blue.stop()            












