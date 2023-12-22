from vpn_core import VPNRule, VPNBody, UserClient


class RestrictVLAN(VPNRule):
    def __init__(self, name, ip, port, id_vlan):
        super().__init__(name, 0, ip, port, id_vlan)
        self.__id_vlan = id_vlan

    def check(self, user: UserClient, body: VPNBody) -> bool:
        dest_ip = '127.0.0.1' if body.dest_ip == 'localhost' else body.dest_ip
        return user.id_vlan != self.__id_vlan or dest_ip != self.ip or self.port != body.dest_port

    def dict_to_obj(dict):
        name = dict['name']
        ip = dict['ip']
        port = dict['port']
        id_vlan = dict['e_id']

        value = RestrictVLAN(name, ip, port, id_vlan)

        return value


class RestrictUser(VPNRule):
    def __init__(self, name, ip, port, user_id):
        super().__init__(name, 1, ip, port, user_id)
        self.__user_id = user_id

    def check(self, user: UserClient, body: VPNBody) -> bool:
        dest_ip = '127.0.0.1' if body.dest_ip == 'localhost' else body.dest_ip
        return user.id != self.__user_id or dest_ip != self.ip or self.port != body.dest_port

    def dict_to_obj(dict):
        name = dict['name']
        ip = dict['ip']
        port = dict['port']
        user_id = dict['e_id']

        value = RestrictUser(name, ip, port, user_id)

        return value
