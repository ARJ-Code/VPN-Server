from udp import UDP
from tcp import TCP
import sys

server_tcp = TCP('localhost', 5002)
server_udp = UDP('localhost', 5002)

args = sys.argv[1:]

if len(args) == 0:
    print("Invalid protocol")
    exit()

if args[0] == 'tcp':
    print('Server TCP started\n')
    for i in server_tcp.run():
        print(f'Received: {i}\n')
elif args[0] == 'udp':
    print('Server UDP started\n')
    for i in server_udp.run():
        print(f'Received: {i}\n')
else:
    print("Invalid protocol")
