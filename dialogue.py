#!/usr/bin/python3

import argparse
from core.server import Server

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", action="store", type=str, help="specify the hostname to use")
    parser.add_argument("port", action="store", type=int, help="specify port to use")
    parser.add_argument("-s", "--server", action="store_true", help="run as server")
    parser.add_argument("-u", "--udp", action="store_true", help="use UDP socket (default is TCP)")
    parser.add_argument("-v", "--verbose", action="store_true", help="set verbosity mode")
    args = parser.parse_args()

    if args.server:
        if args.udp:
            server = Server(args.hostname, "udp", args.port)
        else:
            server = Server(args.hostname, "tcp", args.port)

        server.start()


