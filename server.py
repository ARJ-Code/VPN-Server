from udp import UDP

server = UDP('localhost', 8000)

for i in server.bind():
    print(i)
