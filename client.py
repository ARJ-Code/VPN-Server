from udp import UDP
from tcp import TCP
from vpn import VPNBody
import json

user = input("Introduce the user: ")
password = input("Introduce the password: ")
dest_ip = input("Introduce the destination ip: ")
dest_port = int(input("Introduce the destination port: "))
data = input("Introduce the data: ")

client = TCP('localhost', 5000)

body = VPNBody(user, password, dest_ip, dest_port, data)
body = json.dumps(body, default=lambda o: o.__dict__)

client.send(body, ('localhost', 5001))
