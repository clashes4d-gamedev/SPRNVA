import socket
import _thread as thread

class Server:
    def __init__(self, host=socket.gethostname(), port=42069) -> None:
        self.S = socket.socket()
        self.host = host
        self.port = port

        self.S.bind((self.host, self.port))
        self.S.listen()

        self.connections = []

        self.active = True
        print('[SERVER] Initialization completed successfully!')
        print(f'[SERVER] Listening for connections on: {self.host} on port {self.port}')

    def on_connection(self, connection, address):
        print(f'[SERVER] New connection from {address}.')
        while True:
            msg = connection.recv(1024)
            print(msg)
            if msg == 'STOPCN':
                print('A User disconnected')
                break
        connection.close()

    def start(self):
        while self.active:
            c, addr = self.S.accept()
            thread.start_new_thread(self.on_connection, (c, addr))
        self.S.close()
      
    def stop(self):
        self.active = False

class Client:
    def __init__(self, server='Main') -> None:
        self.server_list = {'Main': ('127.0.0.1', 42069)}

        self.S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.S.setblocking(False)
        self.S.connect_ex(self.server_list[server])

    def disconnect(self):
        self.S.send('STOPCN'.encode('UTF-8'))
