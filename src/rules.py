from vpn_core import VPNRule, VPNBody, UserClient


class RestrictVLAN(VPNRule):
    def __init__(self, name, ip, id_vlan):
        super().__init__(name, 0, ip, id_vlan)
        self.__id_vlan = id_vlan
        # self.__ip = '127.0.0.1' if ip == 'localhost'else ip

    def check(self, user: UserClient, body: VPNBody) -> bool:
        dest_ip = '127.0.0.1' if body.dest_ip == 'localhost' else body.dest_ip
        return user.id_vlan != self.__id_vlan or dest_ip != self.ip
    
    def dict_to_obj(dict):
        name = dict['name']
        _type = dict['type']
        ip = dict['ip']
        id_vlan = dict['e_id']

        value = RestrictVLAN(name, _type, ip, id_vlan)

        return value


class RestrictUser(VPNRule):
    def __init__(self, name, ip, user_id):
        super().__init__(name, 1, ip, user_id)
        self.__user_id = user_id
        # self.__ip = '127.0.0.1' if ip == 'localhost'else ip

    def check(self, user: UserClient, body: VPNBody) -> bool:
        dest_ip = '127.0.0.1' if body.dest_ip == 'localhost' else body.dest_ip
        return user.id != self.__user_id or dest_ip != self.ip
    
    def dict_to_obj(dict):
        name = dict['name']
        _type = dict['type']
        ip = dict['ip']
        user_id = dict['e_id']

        value = RestrictUser(name, _type, ip, user_id)

        return value
