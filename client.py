from udp import UDP

client = UDP('localhost', 5000)

client.send('hola', ('localhost', 8000))
