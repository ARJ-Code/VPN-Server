import os
import json
from udp import UDP


class UserClient:
    def __init__(self, user: str, password: str, id_vlan: int):
        self.user = user
        self.password = password
        self.id_vlan = id_vlan
        self.id = 0

    @staticmethod
    def dict_to_obj(dict):
        user = dict['user']
        password = dict['password']
        id_vlan = dict['id_vlan']

        value = UserClient(user, password, id_vlan)
        value.id = dict['id']

        return value


class VPNBody:
    def __init__(self, user: str, password: str, dest_ip: str, dest_port: int, data: str):
        self.user = user
        self.password = password
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.data = data

    @staticmethod
    def dict_to_obj(dict):
        user = dict['user']
        password = dict['password']
        dest_ip = dict['dest_ip']
        dest_port = dict['dest_port']
        data = dict['data']

        value = VPNBody(user, password, dest_ip, dest_port, data)

        return value


class VPN:
    def __init__(self, ip, port) -> None:
        self.__data = VPN.__read_data()
        self.__udp = UDP(ip, port)

    def create_user(self, user: UserClient):
        if any(user.user == i.user for i in self.__data):
            print('User already registered\n')

            return

        user.id = len(self.__data)
        self.__data.append(user)

        self.__save_data()

        print('User registered\n')

    def remove_user(self, user_id: int):
        if user_id < 0 or user_id >= len(self.__data):
            print('User not found\n')

            return

        new_data = []
        ind = 0

        for i in self.__data:
            if i.id != user_id:
                i.id = ind
                ind += 1

                new_data.append(i)

        self.__data = new_data
        self.__save_data()

        print('User removed\n')

    def run(self):
        print('VPN started\n')

        for i in self.__udp.run():
            try:
                body = VPNBody.dict_to_obj(json.loads(i))
                self.__request(body)
            except:
                continue

    def stop(self):
        self.__udp.stop()
        print('VPN stopped\n')

    def show_users(self):
        for i in self.__data:
            print(
                f'Id: {i.id} User: {i.user} Password: {i.password} Id_VLAN: {i.id_vlan}')
        print()

    def __request(self, body: VPNBody):
        user = next(
            (i for i in self.__data if i.user == body.user and i.password == body.password), None)

        if user is None:
            print('User not found\n')

            return

        self.__udp.send(body.data, (body.dest_ip, body.dest_port))

    @staticmethod
    def __read_data():
        path: str = 'data.json'
        if not os.path.exists(path):
            return []

        try:
            file = open(path, 'r')
            data = json.load(file)
            file.close()

            return [UserClient.dict_to_obj(i) for i in data]
        except:
            return []

    def __save_data(self):
        path = 'data.json'

        file = open(path, 'w')
        json.dump(self.__data,  file, default=lambda o: o.__dict__)
        file.close()
