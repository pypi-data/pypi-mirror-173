# RATCatcher
### _ratcatcher_
Ratcatcher is a tool designed for monitoring and collecting suspicious socket connections, intended for use during the dyanmic analysis of malware. Optionally, it can also capture any packets exchanged during monitoring and output them to a PCAP file, for more a in-depth analysis in Wireshark.
### _omniserver_
WIP. Omniserver is a script for replicating various types of backdoor traffic. Currently it just listens and beacons, possible updates in the future.
## Basic Usage
### Ratcatcher
```
usage: ratcatcher [-h] [-f SECONDS] [-b CYCLES] [--capture FILENAME]
                  [{inet,inet4,inet6,tcp,tcp4,tcp6,udp,udp4,udp6,unix,all}]
                  
positional arguments:
  {inet,inet4,inet6,tcp,tcp4,tcp6,udp,udp4,udp6,unix,all}
                        Type of traffic to monitor (Default: all)
                        
options:
  -h, --help            show this help message and exit
  -f SECONDS, --frequency SECONDS
                        Frequency, in seconds, to check for active connections (Default: 1.0)
  -b CYCLES, --baseline CYCLES
                        Collect a baseline of traffic, to help filter out normal processes (Total time =
                        frequency*CYCLES)
  --capture FILENAME    Capture packets during monitoring and output to PCAP file
  
Examples:
    ratcatcher (Monitor all traffic types)
    ratcatcher --baseline 10 -f .5 --capture mypackets
    ratcatcher inet6
```
### Omniserver 
```
usage: omniserver [-h] [-b IPADDR] [-f SECONDS] [-t SECONDS] [-d] [-u] [--msg MSG] [port]

positional arguments:
  port                  Port to listen on/connect to (Default: RHP for listen/beacon, 53 for DNS)
  
options:
  -h, --help            show this help message and exit
  -b IPADDR, --beacon IPADDR
                        Beacon to remote IP
  -f SECONDS, --frequency SECONDS
                        Frequency, in seconds, to beacon remote IP
  -t SECONDS, --timeout SECONDS
                        Timeout duration, in seconds, for beacon sockets
  -d, --dns             Send DNS requests
  -u, --udp             Use UDP protocol (Default: TCP)
  --msg MSG             Message to send upon successful connection
  
Examples:
    omniserver (Listen on TCP random high port)
    omniserver -b 10.10.10.1 -f 30 -u 7896
    omniserver --msg 'TCP Server Test Message'
```
## Installation

Install from PyPI
```
pip install ratcatcher
```
## Known Issues & TODO
- Ratcatcher is completely unaware of outgoing UDP packets. However they're still caught in the PCAP
- Add DNS tunneling to omniserver
