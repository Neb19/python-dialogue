
import threading
import logging

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
        self.send("-------------------------------------------")
        self.send("\nWelcome to Dialoguer, a simple Python Chat!")
        self._loop()


    def send(self, data:str) ->bool:
        try:
            self.conn.send(data.encode('utf-8'))
        except:
            return False

        return True


    def send_to_all(self, data:str):
        logging.info('data received')
        if SessionTCPHandler.total_sessions > 1:
            targetSessions = SessionTCPHandler.sessions
            targetSessions.remove(self)
            for session in targetSessions:
                session.send(data.decode('utf-8'))

            targetSessions.append(self)


    def receive(self) -> str:
        return self.conn.recv(1024)


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
