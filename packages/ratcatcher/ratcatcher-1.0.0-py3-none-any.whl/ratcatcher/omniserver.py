#
# Copyright (C) 2022 LLCZ00
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.  
#

"""
Tool for testing remote connection methods
- DNS Tunnel
"""
import argparse
import socket, socketserver
import sys
import time
import traceback
import threading


"""
Core Networking Classes
"""
class ServerHandler:
    """
    Allows socketserver.BaseRequestHandler to accept arguments, 
    returns the appropriate protocol instance for server tasks
    """
    def __init__(self, msg, udp=False, buffersize=1024, callback=None):
        self.msg = msg
        self.udp = udp
        self.buffersize = buffersize
        self.callback = callback
        
    def __call__(self, request, address, server): # for socketserver.TCPServer/UDPServer
        if self.udp:
            return UDPServer(request, address, server, self)
        return TCPServer(request, address, server, self)


class UDPServer(socketserver.BaseRequestHandler):  
    def __init__(self, request, address, server, server_handle):
        self.server_handle = server_handle
        super().__init__(request, address, server)
        
    def handle(self):
        try:
            self.client = f"{self.client_address[0]}:{self.client_address[1]}"
            data = self.request[0].strip()
            response = self.server_handle.msg           
            if data:
                print(f"[{self.client}] Data recieved: {data.decode()}")               
                if self.server_handle.callback:
                    response = self.server_handle.callback(data, response)                    
                if response is not None:
                    self.request[1].sendto(self.encode_data(response), self.client_address)
                    print(f"[{self.client}] Response sent.\n")
                    
        except Exception:
            traceback.print_exc(file=sys.stderr)
        
    def encode_data(self, data, encoding="utf-8"):
        if type(data) is not bytes:
            data = f"{data}\n".encode(encoding)
        return data


class TCPServer(socketserver.BaseRequestHandler):
    def __init__(self, request, address, server, server_handle):
        self.server_handle = server_handle
        super().__init__(request, address, server)
        
    def handle(self):
        self.client = f"{self.client_address[0]}:{self.client_address[1]}"
        print(f"[OMNI] Connection from {self.client}")
        try:
            while True:
                data = self.request.recv(self.server_handle.buffersize).strip()
                if not data:
                    break
                print(f"[{self.client}] Data recieved: {data.decode()}")
                response = self.server_handle.msg
                if self.server_handle.callback:
                    response = self.server_handle.callback(data, response)
                if response is not None:
                    self.request.sendall(self.encode_data(response))
                    print(f"[{self.client}] Response sent.")
            print(f"[{self.client}] Connection closed.\n")
            
        except Exception:
            traceback.print_exc(file=sys.stderr)
        
    def encode_data(self, data, encoding="utf-8"):
        if type(data) is not bytes:
            data = f"{data}\n".encode(encoding)
        return data


class BeaconHandler:
    def __init__(self, ip, port, timeout=5, udp=False, buffersize=1024, msg=""):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.udp = udp
        self.buffersize = buffersize
        self.msg = msg
        self.server = f"{ip}:{port}"
        self.sock = None
        
    def open(self):
        if self.sock is None:
            if self.udp:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            
    def close(self):
        if self.sock is not None:
            self.sock.close()
            
    def beacon(self, data=None):
        if data is None:
            data = self.msg
        if self.udp:
            self.sock.sendto(self.encode_data(data), (self.ip, self.port))
            print(f"[OMNI] UDP Beacon sent to {self.server}")
        else:
            try:
                print(f"[OMNI] Attempting TCP connection to {self.server}...", end='') 
                self.sock.connect((self.ip, self.port))
                self.sock.sendall(self.encode_data(data))
            except (socket.timeout, ConnectionRefusedError, ConnectionResetError):
                print("failed")
                return False
            else:
                print("success")
        return True
            
    def get_data(self):
        try:
            data = self.sock.recv(self.buffersize).strip()
        except (socket.timeout, ConnectionRefusedError, ConnectionResetError):
            print("Timeout/no response")
            return None
        else:
            print(f"[{self.server}] Data recieved: {data.decode()}")
            return data
        
    def encode_data(self, data, encoding="utf-8"):
        if type(data) is not bytes:
            data = f"{data}\n".encode(encoding)
        return data

"""
Core Functions
"""
def create_listener(port=0, udp=False, msg="Test Message"):
    listen_ip = "0.0.0.0"
    if udp:
        server = socketserver.ThreadingUDPServer((listen_ip, port), ServerHandler(msg, udp=udp))
    else:
        server = socketserver.ThreadingTCPServer((listen_ip, port), ServerHandler(msg, udp=udp))
    
    server.allow_reuse_address = True
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True  # exit the server thread when the main thread terminates
    thread.start()
    
    conntype = "TCP"
    if udp:
        conntype = "UDP"

    print(f"[OMNI] {conntype} Server listening on {server.server_address[0]}:{server.server_address[1]}...\n")
    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        print("[OMNI] Server closed.")    

def create_beacon(dest_ip, port, frequency=5, max_tries=5, timeout=5, udp=False, msg="", callback=None):
    local_socket = BeaconHandler(ip=dest_ip, port=port, timeout=timeout, udp=udp, msg=msg)
    print(f"[OMNI] Beaconing {local_socket.server} every {frequency}s...\n")
    
    local_socket.open()
    tries = 0
    while tries < max_tries:        
        if local_socket.beacon():
            data = local_socket.get_data()
            if data:
                if callback:
                    data = callback(data)
                break
            if not udp:
                break
        
        time.sleep(frequency)
        tries += 1
    
    local_socket.close()
    print("\n[OMNI] Beacon ceased.")

def create_dns(port):
    pass

def main():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Remote Connection Tests', 
    epilog='Examples:\n\tomniserver (Listen on TCP random high port)\n\tomniserver -b 10.10.10.1 -f 30 -u 7896\n\tomniserver --msg \'TCP Server Test Message\''
    )
    parser.add_argument(
        '-b', '--beacon', 
        metavar='IPADDR',
        dest='beacon_ip',
        help='Beacon to remote IP'
    )
    parser.add_argument(
        '-f', '--frequency', 
        metavar='SECONDS',
        dest='freq',
        type=int,
        default=5,
        help='Frequency, in seconds, to beacon remote IP'
    )
    parser.add_argument(
        '-t', '--timeout', 
        metavar='SECONDS',
        dest='timeout',
        type=int,
        default=5,
        help='Timeout duration, in seconds, for beacon sockets'
    )
    parser.add_argument(
        '-d', '--dns', 
        dest='dns_flag',
        action='store_true',
        help='Send DNS requests'
    )
    parser.add_argument(
        '-u', '--udp', 
        dest='udp_flag',
        action='store_true',
        help='Use UDP protocol (Default: TCP)'
    )
    parser.add_argument(
        '--msg', 
        type=str,
        default="testRAT connection message",
        help='Message to send upon successful connection'
    )
    parser.add_argument(
        'port',
        nargs='?',
        type=int,
        default=0,
        help='Port to listen on/connect to (Default: RHP for listen/beacon, 53 for DNS)'
    )
    args = parser.parse_args()
    if args.beacon_ip:
        create_beacon(dest_ip=args.beacon_ip, port=args.port, frequency=args.freq, timeout=args.timeout, udp=args.udp_flag, msg=args.msg)
        
    elif args.dns_flag:
        if args.port == 0:
            args.port = 53
        create_dns(args.port)
        
    else:
        create_listener(port=args.port, udp=args.udp_flag, msg=args.msg) 
    

if __name__ == "__main__":
    pass
     
      
        
    

