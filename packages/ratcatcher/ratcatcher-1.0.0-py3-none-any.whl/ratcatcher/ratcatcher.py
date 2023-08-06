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
RATCatcher
Monitor and collect suspicious traffic
"""
import psutil
import time
import argparse
from scapy.all import AsyncSniffer, wrpcap


# scapy.wrpcap(r"C:\Users\IEUser\Desktop\ratcatcher\booty.pcap", capture)


conn_kind = { # Enum for psutil net_connection types
    "inet" : "IPv4 and IPv6",
    "inet4" : "IPv4",
    "inet6" : "IPv6",
    "tcp" : "TCP",
    "tcp4" : "TCP over IPv4",
    "tcp6" : "TCP over IPv6",
    "udp" : "UDP",
    "udp4" : "UDP over IPv4",
    "udp6" : "UDP over IPv6",
    "unix" : "unix socket",
    "all" : "all possible"
}

proto_type = { # Enum for psutil protocol types
    1 : "TCP",
    2 : "UDP",
    3 : "OTHER" # Just in case
}

class RatCatcher:
    def __init__(self, kind: str = "all", frequency: float = 1, capture=False):
        self.kind = kind
        self.frequency = frequency
        self.baseline_traffic = []
        self.capture = capture
        
    def collect_baseline(self, cycles: int = 5):
        """Monitor network traffic for appx. cycles*frequency seconds, to collect a baseline of normal traffic"""
        if cycles == 0:
            return None
        print(f"[RC] Collecting baseline {conn_kind[self.kind]} traffic (appx. {cycles*self.frequency} seconds)...")        
        self.baseline_traffic = psutil.net_connections(self.kind)
        cycle = 0
        while cycle < cycles:
            for conn in psutil.net_connections(self.kind):
                if conn not in self.baseline_traffic:
                    self.baseline_traffic.append(conn)
            cycle += 1
            time.sleep(self.frequency)            
        print(f"[RC] Baseline complete - {len(self.baseline)} connections collected.")
               
    def monitor_traffic(self):
        """Monitor traffic for new active socket connections"""
        if not self.baseline_traffic: # If no baseline collected, use current list of network connections
            self.baseline_traffic = psutil.net_connections()
        if self.capture:
            sniffer = AsyncSniffer()
            sniffer.start()            
        print(f"[RC] Monitoring {conn_kind[self.kind]} connections...\n(Ctrl-c) to cease monitoring)")
        try:
            while True:
                for conn in psutil.net_connections():
                    if conn not in self.baseline_traffic:
                        self.baseline_traffic.append(conn)
                        new_connection = f"[{proto_type[conn.type]}] {conn.laddr[0]}:{conn.laddr[1]}"
                        if conn.raddr:
                            new_connection += f"-> {conn.raddr[0]}:{conn.raddr[1]}"
                        print(f"{new_connection}\nStatus: {conn.status}\nPID: {conn.pid}")
                        try:
                            proc = psutil.Process(conn.pid)
                            print(f"Process name: {proc.name()}\nExe path: {proc.exe()}\nCommand line: {' '.join(proc.cmdline())}\n")
                        except:
                            pass
                                               
                time.sleep(self.frequency)
                
        except KeyboardInterrupt:
            pass
        print(f"[RC] Monitoring complete.")
        if self.capture:
            packets = sniffer.stop()
            wrpcap(self.capture+'.pcap', packets)
            print(f"[RC] Packets captured and output to {self.capture+'.pcap'}\n{packets}")
                 
    

def main():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Monitor and collect suspicious network traffic',
    epilog='Examples:\n\tratcatcher (Monitor all traffic types)\n\tratcatcher --baseline 10 -f .5 --capture mypackets\n\tratcatcher inet6'
    )
    parser.add_argument(
        '-f', '--frequency', 
        metavar='SECONDS',
        dest='freq',
        type=float,
        default=1,
        help='Frequency, in seconds, to check for active connections (Default: 1.0)'
    )
    parser.add_argument(
        '-b', '--baseline', 
        metavar='CYCLES',
        dest='cycles',
        type=int,
        default=0,
        help='Collect a baseline of traffic, to help filter out normal processes (Total time = frequency*CYCLES)'
    )
    parser.add_argument(
        '--capture', 
        metavar='FILENAME',
        dest='pcap',
        default=None,
        help='Capture packets during monitoring and output to PCAP file'
    )
    parser.add_argument(
        'kind',
        choices = ["inet", "inet4", "inet6", "tcp", "tcp4", "tcp6", "udp", "udp4", "udp6", "unix", "all"],
        nargs='?',
        type=str,
        default="all",
        help='Type of traffic to monitor (Default: all)'
    )
    args = parser.parse_args()
    rc = RatCatcher(kind=args.kind, frequency=args.freq, capture=args.pcap)
    rc.collect_baseline(args.cycles)
    rc.monitor_traffic()


if __name__ == "__main__":
    pass
    