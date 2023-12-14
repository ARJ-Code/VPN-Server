import os
import json


class UserClient:
    def __init__(self, user: str, password: str, id_vlan: int) -> None:
        self.user = user
        self.password = password
        self.id_vlan = id_vlan


class VPN:
    def __init__(self) -> None:
        self.__data = VPN.__read_data()

    def register(self, user: UserClient):
        self.__data.append(user)

        self.__save_data()

    def __read_data():
        path: str = 'data.json'
        if not os.path.exists(path):
            return []

        try:
            file = open(path, 'r')
            data = json.load(file)
            file.close()
            if isinstance(data, list) and all(VPN.__is_register_client(i) for i in data):
                return data
            else:
                return []
        except:
            return []

    def __is_register_client(obj):
        return 'user' in obj and 'password' in obj and 'id_vlan' in obj

    def __save_data(self):
        path = 'data.json'

        file = open(path, 'w')
        json.dump(self.__data,  file, default=lambda o: o.__dict__)
        file.close()
