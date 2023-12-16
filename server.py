from udp import UDP

server = UDP('localhost', 5002)

print('Server started\n')

for i in server.bind():
    print(f'Received: {i}\n')
