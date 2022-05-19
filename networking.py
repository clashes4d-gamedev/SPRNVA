import socket
import _thread as thread


class Server:
    # TODO add a function parameter to the on_connect function in wich the user can specify a function to run every server tick
    def __init__(self, host=socket.gethostname(), port=42069) -> None:
        self.S = socket.socket()
        self.host = socket.gethostbyname(host)
        self.port = port
        self.block_size = 2048
        self.encoding = 'utf-8'

        self.S.bind((self.host, self.port))
        self.S.listen()

        self.connections = {}

        self.active = True
        self.msg = b''
        print('[SERVER] Initialization completed successfully!')
        print(f'[SERVER] Listening for connections on: {self.host} on port {self.port}')

    def send(self, connection, msg: str):
        if len(msg.encode(self.encoding)) <= self.block_size:
            connection.send(msg.encode(self.encoding))
        else:
            return -1

    def receive(self, connection):
        return connection.recv(self.block_size).decode(self.encoding)

    def on_connection(self, connection, address, handle_func):
        print(f'[SERVER] New connection from {address}.')
        self.send(connection, str(self.block_size))
        self.send(connection, self.encoding)

        # appends the user to the list of active connections
        if len(self.connections) == 0:
            conn_id = '0'
            self.connections[conn_id] = [connection]
        else:
            conn_id = int(len(self.connections))
            self.connections[str(conn_id)] = [connection]

        while True:
            self.msg = self.receive(connection)

            try:
                handle_func(conn_id, self.connections, connection, self.msg)
            except ConnectionResetError:
                print('[SERVER] Connection has been reset by Client. Shutting down this Client-Thread.')
                connection.close()
                self.connections.pop(conn_id)
                self.stop()

            if self.msg == ':STOP':
                print(f'[SERVER] {conn_id} on {address} disconnected')
                break

        connection.close()
        self.connections.pop(conn_id)

    def start(self, handle_func):
        while self.active:
            c, addr = self.S.accept()
            thread.start_new_thread(self.on_connection, (c, addr, handle_func))
        self.S.close()
      
    def stop(self):
        self.active = False


class Client:
    def __init__(self, server='Main') -> None:
        self.server_list = {'Main': (socket.gethostname(), 42069)}

        self.S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.S.connect_ex(self.server_list[server])

        self.block_size = int(self.S.recv(4).decode())
        self.block_encoding = self.S.recv(self.block_size).decode()

    def send(self, msg: str):
        if len(msg.encode(self.block_encoding)) <= self.block_size:
            self.S.send(msg.encode(self.block_encoding))
        else:
            return -1

    def receive(self, flush=False):
        if flush is False:
            return self.S.recv(self.block_size).decode(self.block_encoding)
        else:
            if self.S.recv(self.block_size) == b'':
                return

    def flush(self):
        print('[CLIENT] Flushing Server stream ...')
        self.S.recv(self.block_size)
        print('[CLIENT] Server stream Flushed successfully.')

    def disconnect(self):
        self.send(':STOP')
