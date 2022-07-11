import socket
import select
import _thread as thread

class Server:
    def __init__(self, host=socket.gethostname(), port=42069, block_size=2048, encoding='utf-8', max_connections=0) -> None:
        self.S = socket.socket()
        self.host = socket.gethostbyname(host)
        self.port = port
        self.block_size = block_size
        self.encoding = encoding
        self.max_connections = max_connections

        self.S.bind((self.host, self.port))
        #self.S.setblocking(False)
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
            conn_id = str(int(len(self.connections)))
            self.connections[conn_id] = [connection]

        while True:
            self.msg = self.receive(connection)

            try:
                handle_func(conn_id, self.connections, connection, self.msg)
            except ConnectionResetError:
                print('[SERVER] Connection has been reset by Client. Shutting down this Client-Thread.')
                self.connections.pop(conn_id)
                connection.close()
                self.stop()

            if self.msg == ':STOP':
                print(f'[SERVER] {conn_id} on {address} disconnected')
                break

            #print(self.connections)
        self.connections.pop(conn_id)
        connection.close()

    def start(self, handle_func):
        try:
            while self.active:
                if self.max_connections != 0:
                    if len(self.connections.keys()) <= self.max_connections:
                        print(len(self.connections.keys()))
                        c, addr = self.S.accept()
                        thread.start_new_thread(self.on_connection, (c, addr, handle_func))
                    else:
                        c, addr = self.S.accept()
                        c.close()
                else:
                    c, addr = self.S.accept()
                    thread.start_new_thread(self.on_connection, (c, addr, handle_func))
            self.S.close()
        except KeyboardInterrupt as e:
            print(f'[SERVER] Shutting down Server because of KeyboardInterrupt.')
            self.stop()
      
    def stop(self):
        self.active = False


class Client:
    def __init__(self, server='Main') -> None:
        self.server_list = {'Main': (socket.gethostname(), 42069)}

        self.S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.S.setblocking(False)
        #self.S.settimeout(10)
        self.S.connect_ex(self.server_list[server])

        r, _, _ = select.select([self.S], [], [])
        if r:
            self.block_size = int(self.S.recv(4).decode())

            self.block_encoding = self.S.recv(self.block_size).decode()

    def send(self, msg: str):
        if len(msg.encode(self.block_encoding)) <= self.block_size:
            self.S.send(msg.encode(self.block_encoding))
        else:
            return -1

    def receive(self, flush=False):
        if flush is False:
            r, _, _ = select.select([self.S], [], [])
            if r:
                return self.S.recv(self.block_size).decode(self.block_encoding)
        else:
            r, _, _ = select.select([self.S], [], [])
            if r:
                if self.S.recv(self.block_size) == b'':
                    return


    def disconnect(self):
        self.send(':STOP')
