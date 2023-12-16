from vpn import VPN, UserClient
import threading


def help():
    print("help: Show the commands")
    print("create_user <user> <password> <id_vlan>: Create a new user")
    print('remove_user <id>: Remove a user')
    print('show_users: Show all users')
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
    command = command.split(' ')

    if len(command) == 0:
        print("Invalid command\n")

    if command[0] == "create_user" and len(command) == 4 and str.isdigit(command[3]):
        user = command[1]
        password = command[2]
        id_vlan = int(command[3])
        vpn.create_user(UserClient(user, password, id_vlan))

    elif command[0] == "remove_user" and len(command) == 2 and str.isdigit(command[1]):
        vpn.remove_user(int(command[1]))

    elif command[0] == "show_users":
        vpn.show_users()

    elif command[0] == "start":
        if (vpn_thread is not None):
            print("VPN already started\n")
            continue
        vpn_thread = threading.Thread(target=vpn.run)
        vpn_thread.start()

    elif command[0] == "stop":
        if (vpn_thread is None):
            print("VPN not started\n")
            continue
        vpn.stop()
        vpn_thread.join()
        vpn_thread = None

    elif command[0] == "exit":
        break

    elif command[0] == "help":
        help()
    else:
        print("Invalid command\n")
