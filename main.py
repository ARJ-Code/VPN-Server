from vpn import VPN, UserClient

a = VPN('localhost', 5000)

a.register(UserClient('a', 'a', 1))
a.register(UserClient('a', 'a', 1))
