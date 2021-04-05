
import threading
import logging
import time

class SessionTCPHandler(threading.Thread):

    # format logging text
    logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

    sessions = []
    total_sessions = 0

    def __init__(self, conn, addr):
        self._thread = threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr


    """
    Override run() from Thread class.
    Called when <object>.start() is called to run/start the thread.
    """
    def run(self):
        SessionTCPHandler.sessions.append(self)
        SessionTCPHandler.total_sessions += 1
        logging.info("active sessions : {}".format(SessionTCPHandler.total_sessions))
        self.welcome()

    def welcome(self):
        self.send("-------------------------------------------")
        time.sleep(0.1)
        self.send("Welcome to Dialoguer!")
        time.sleep(0.1)
        self.send("What's your name ?")
        time.sleep(0.1)
        self.username = self.receive()

        for user in SessionTCPHandler.sessions:
            user.send("[{}] is now connected.".format(self.username.decode('utf-8')))

        self._loop()


    """
    Send data to the client
    """
    def send(self, data:str) ->bool:
        self.conn.send(data.encode('utf-8'))
        return True


    """
    Send data to all connected clients
    """
    def send_to_all(self, data:str):
        logging.info('data received')
        for session in SessionTCPHandler.sessions:
            session.send(self.username.decode('utf-8') + ": " + data.decode('utf-8'))


    """
    Receive data from client
    """
    def receive(self) -> str:
        try:
            return self.conn.recv(1024)
        except ConnectionResetError:
            logging.info("connection closed by peer {}".format(self.addr))
            SessionTCPHandler.sessions.remove(self)
            SessionTCPHandler.total_sessions -= 1
            logging.info('active session : {}'.format(SessionTCPHandler.total_sessions))


    """
    Loop on client inputs
    Break the loop when client leaves the connection
    """
    def _loop(self):
        while True:
            conn_input = self.receive()
            if not conn_input:
                break
            self.send_to_all(conn_input)

        SessionTCPHandler.sessions.remove(self)
        SessionTCPHandler.total_sessions -= 1
        logging.info('user disconnected')
        logging.info('active session : {}'.format(SessionTCPHandler.total_sessions))

