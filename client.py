from udp import UDP
from tcp import TCP
from vpn import VPNBody
import json
import sys

user = input("Introduce the user: ")
password = input("Introduce the password: ")
dest_ip = input("Introduce the destination ip: ")
dest_port = int(input("Introduce the destination port: "))
data = input("Introduce the data: ")

client_tcp = TCP('localhost', 5000)
client_udp = UDP('localhost', 5000)

body = VPNBody(user, password, dest_ip, dest_port, data)
body = json.dumps(body, default=lambda o: o.__dict__)

args = sys.argv[1:]

if len(args) == 0:
    print("Invalid protocol")
    exit()

if args[0] == 'tcp':
    client_tcp.send(body, ('localhost', 5001))
elif args[0] == 'udp':
    client_udp.send(body, ('localhost', 5001))
else:
    print("Invalid protocol")
