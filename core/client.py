
import socket
import threading

class Client:
    """
    Client class to connect to the server
    """

    def __init__(self, hostname:str, protocol:int, port:int) -> None:
        self.hostname = hostname
        self.protocol = protocol.lower()
        self.port     = port
        self._socket   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    """
    Connect to the server, execute 2 thread to receive and send data
    """
    def connect(self):
        self._socket.connect((self.hostname, self.port))
        recvThread = threading.Thread(target=Client._recvDataFromServer, args=(self,))
        sendThread = threading.Thread(target=Client._sendDataToServer, args=(self,))
        recvThread.start()
        sendThread.start()

    """
    Called in a thread
    """
    def _recvDataFromServer(self):
        while True:
            data_from_server = self._socket.recv(1024)
            if not data_from_server:
                break
            print(data_from_server.decode('utf-8'))

    """
    Called in a thread
    """
    def _sendDataToServer(self):
        while True:
            data = input()
            self._socket.send(data.encode('utf-8'))
            if not data:
                break

