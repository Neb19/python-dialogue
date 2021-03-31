#!/usr/bin/python3 -d

import logging
import socket
import threading

"""
This class provides the necessary to manage a tcp or udp server.
Each instance is a server configuration with usual attributes like :
    * port to use
    * hostname (localhost, 192.168.1.10, etc)
    * protocol (udp, tcp)
When your server class object is initialized, you can start, stop, restart the server.

A new system thread is created each time you want to start a server configuration,
and each time a new connection is incoming.
"""
class Server:

    # format logging text
    logging.basicConfig(format="[%(asctime)s] %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

    # contains all thread executed by each server/object instances
    active_server_threads = []

    # used to close a child thread, class attribute
    stop_thread = None

    """
    Server Initialization
        Parameters:
            hostname  (string)  : interface to listen
            protocol  (string)  : protocol to use
            port      (integer) : port to use
            thread_id (integer) : contain the thread_id when .start() method is called
    """
    def __init__(self, hostname, protocol, port):
        self.hostname = hostname
        self.protocol = protocol.lower()
        self.port  = int(port)
        self.thread_id = None
        self.clients = []


    # Start the server in a different thread
    def start(self):
        thread = threading.Thread(target=Server.__listen, args=(self,))
        thread.start()


    # Stop the server
    def stop(self):
        logging.info('stopping the server...')
        self.__close()


    # Restart the server
    def restart(self):
        self.stop()
        self.start()


    # Handle connection interraction with the client
    def handle_connectionTCP(self, client):
        with client:
            client.send("Welcome!\n".encode('utf-8'))
            client.send("are you ok ?\n".encode('utf-8'))
            while True:
                data = client.recv(1024)
                data = data.decode('utf-8').rstrip()
                if not data:
                    break

                logging.info('receive message from client: ' + data)
                if data == "yes":
                    client.send("great!\n".encode('utf-8'))

                elif data == "no":
                    client.send("sad:(\n".encode('utf-8'))
                else:
                    pass


    def handle_connectionUDP(self, client):
        print(client)



    # This method creates the socket, binds the hostname, and loops on incoming socket connections
    def __listen(self):
        logging.info('starting {}:{}/{}'.format(self.hostname, self.port, self.protocol))

        # set the thread id to the object, as a running server thread. This is useful to close the thread later
        self.thread_id = threading.get_ident()
        # append the thread id to the class attribute in order to list all running threads later
        Server.active_server_threads.append(self.thread_id)

        # define the socket type to use
        if self.protocol == "tcp":
            socket_proto = socket.SOCK_STREAM
        elif self.protocol == "udp":
            socket_proto = socket.SOCK_DGRAM

        # create the socket, bind it to the hostname, and loop on incoming connections
        try:
            server_socket = socket.socket(socket.AF_INET, socket_proto)
            server_socket.bind((self.hostname, self.port))
            if self.protocol == "tcp":
                server_socket.listen(3)
        except:
            logging.error('cannot init server')
        else:
            logging.info('server: started')

        # the "listenning loop" to catch each incoming connections into a new thread
        # if the thread_id attribute is not defined, then break the loop
        while hasattr(self, "thread_id"):
            # accept incoming tcp connections
            if self.protocol == "tcp":
                (client, address) = server_socket.accept()
                t = threading.Thread(target=Server.handle_connectionTCP, args=(self, client))
            elif self.protocol == "udp":
                (client, address) = server_socket.recvfrom(1024)
                t = threading.Thread(target=Server.handle_connectionUDP, args=(self, client))

            # log new connection and handle it in new thread
            logging.info('new connection from : {}'.format(str(address)))
            t.start()

        # out of the listenning loop, so server is stopped
        logging.info("server: stopped")


    # close the thread by unsetting the thread_id object attribute - watched by the listenning loop
    # we must create a new connection to the socket after deleting the attribute in order to..
    # .. trigger the next loop sequence and break it
    def __close(self):
        Server.active_server_threads.remove(self.thread_id)
        del self.thread_id
        close_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        close_conn.connect((self.hostname, self.port))

