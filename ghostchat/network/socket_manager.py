from config import BUFFER_SIZE

class SocketManager:
    def __init__(self, sock):
        self.sock = sock

    def send(self, data: bytes):
        self.sock.sendall(data)

    def receive(self):
        return self.sock.recv(BUFFER_SIZE)
