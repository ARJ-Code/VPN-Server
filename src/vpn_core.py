from abc import ABC, abstractmethod


class NetWorkProtocol(ABC):
    def __init__(self, ip, port):
        self._ip = '127.0.0.1' if ip == 'localhost' else ip
        self._port = port

    @abstractmethod
    def send(self, data, dest_addr):
        pass

    @abstractmethod
    def run(self):
        pass


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


class VPNRule(ABC):
    def __init__(self, name, _type, ip, e_id):
        self.name = name
        self._type = _type
        self.ip = '127.0.0.1' if ip == 'localhost'else ip
        self.e_id = e_id
        self.id = 0

    @abstractmethod
    def check(self, user: UserClient, body: VPNBody):
        pass

    @abstractmethod
    def dict_to_obj(dict):
        pass
