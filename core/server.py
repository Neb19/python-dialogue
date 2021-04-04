
import logging
import threading
import socket
import time
from .session import SessionTCPHandler

class Server:
    """
    This class provides an interface to run a server socket
    and interact with it.
    An initialized object represents a server configuration.
    the start() method run the server in a new thread and
    for each incoming connection a new thread is created.
    """

    # format logging text
    logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

    def __init__(self, hostname:str='127.0.0.1', protocol:str='tcp', port:int=8888, max_conn:int=5) -> None:
        self._hostname   = hostname
        self._protocol   = protocol.lower()
        self._port       = port
        self._maxconn    = max_conn
        self._threadID   = None
        self._socket     = None
        self._socketType = socket.SOCK_DGRAM if self._protocol == "udp" else socket.SOCK_STREAM
        self._sessions   = []


    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def protocol(self) -> str:
        return self._protocol

    @property
    def port(self) -> int:
        return self._port

    @property
    def maxconn(self) -> int:
        return self._maxconn


    """
    Start the server in new thread
    """
    def start(self) -> bool:
        logging.info('starting server: {} on port {}/{}'.format(self._hostname, self._port, self._protocol))
        self._socket = socket.socket(socket.AF_INET, self._socketType)
        try:
            self._socket.bind((self._hostname, self._port))
            if self._protocol == 'tcp':
                self._socket.listen(self._maxconn)
        except:
            logging.error('Cannot bind address on {}:{}/{}'.format(self._hostname, self._port, self._protocol))
            return False

        if self.__createThread(self.__listenLoop):
            logging.info('server is running ({}:{}/{})'.format(self._hostname, self._port, self._protocol))
        else:
            logging.error('Cannot start the server')
            return False

        return True


    """
    Stop the server
    """
    def stop(self) -> bool:
        logging.info('stopping server ...')
        try:
            del self._threadID
            close_conn = socket.socket(socket.AF_INET, self._socketType)
            close_conn.connect((self._hostname, self._port))
        except:
            logging.error('server is not running.')
            return False

        return True


    """
    Restart the server
    """
    def restart(self) -> bool:
        if not self.stop():
            return False

        time.sleep(1)

        if not self.start():
            return False

        return True


    """
    Loop on incoming connections
    Create a new thread for new connections
    """
    def __listenLoop(self) -> bool:
        self._threadID = threading.get_ident()
        while hasattr(self, "_threadID"):
            try:
                (conn, addr) = self._socket.accept()
            except:
                return False

            session = SessionTCPHandler(conn, addr)
            self._sessions.append(session)
            session.start()
#            self.__createThread(self.handleConnectionTCP, (conn,))

        self._socket.close()
        logging.info('socket closed')
        return True


    """
    Method called to handle TCP Connection
    """
    def handleConnectionTCP(self, conn) -> None:

        def loop(conn):
            while True:
                conn_input = conn.recv(1024)
                if not conn_input:
                    break
        return loop


    """
    Method called to handle UDP Connection
    """
    def handleConnectionUDP(self, conn):
        return conn


    """
    Create new Thread for the target function
    """
    def __createThread(self, func, parameters=(None), wait=False) -> bool:
        if parameters == None:
            thread = threading.Thread(target=func)
        else:
            thread = threading.Thread(target=func, args=parameters)

        try:
            thread.start()
        except:
            return False

        if wait == True:
            thread.join()

        return True



if __name__ == "__main__":
    server1 = Server(hostname='localhost', port=2223, max_conn=10, protocol='tcp')
    server1.start()

    #server2 = Server(hostname='localhost', port=2224, max_conn=5, protocol='tcp')
    #server2.start()
    #time.sleep(3)
    #server1.restart()
    #server1.stop()
