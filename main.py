from vpn import VPN, UserClient
import threading


def help():
    print("help: Show the commands")
    print("register: Register a new user")
    print("start: Start the VPN")
    print("stop: Stop the VPN")
    print("exit: Exit the program\n")


ip = 'localhost'
port = 5001

vpn = VPN(ip, port)
vpn_thread = None

print("Welcome to the VPN")
print(f"Running on {ip}:{port} \n")
help()

while True:
    command = input()

    if command == "create_user":
        user = input("Introduce the user: ")
        password = input("Introduce the password: ")
        id_vlan = int(input("Introduce the id vlan: "))
        vpn.register(UserClient(user, password, id_vlan))

    elif command == "start":
        if (vpn_thread is not None):
            print("VPN already started\n")
            continue
        vpn_thread = threading.Thread(target=vpn.run)
        vpn_thread.start()

    elif command == "stop":
        if (vpn_thread is None):
            print("VPN not started\n")
            continue
        vpn.stop()
        vpn_thread.join()
        vpn_thread = None

    elif command == "exit":
        break

    elif command == "help":
        help()
    else:
        print("Invalid command")
