from udp import UDP
from tcp import TCP

server = TCP('localhost', 5002)

print('Server started\n')

for i in server.run():
    print(f'Received: {i}\n')
