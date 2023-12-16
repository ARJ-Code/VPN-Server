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


class VPN:
    def __init__(self, ip, port) -> None:
        self.__data = VPN.__read_data()
        self.__udp = UDP(ip, port)

    def register(self, user: UserClient):
        if any(user.user == i.user for i in self.__data):
            print('User already registered\n')

            return

        user.id = len(self.__data)
        self.__data.append(user)

        self.__save_data()

        print('User registered\n')

    def start(self):
        for i in self.__udp.bind():
            print(i)

    @staticmethod
    def __read_data():
        path: str = 'data.json'
        if not os.path.exists(path):
            return []

        try:
            file = open(path, 'r')
            data = json.load(file)
            file.close()
            if isinstance(data, list) and all(VPN.__is_register_client(i) for i in data):
                return [UserClient.dict_to_obj(i) for i in data if VPN.__is_register_client(i)]
            else:
                return []
        except:
            return []

    @staticmethod
    def __is_register_client(obj):
        return 'id' in obj and 'user' in obj and 'password' in obj and 'id_vlan' in obj

    def __save_data(self):
        path = 'data.json'

        file = open(path, 'w')
        json.dump(self.__data,  file, default=lambda o: o.__dict__)
        file.close()
