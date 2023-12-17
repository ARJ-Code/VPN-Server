from vpn_core import VPNRule, VPNBody, UserClient


class RestrictVLAN(VPNRule):
    def __init__(self, name, ip, id_vlan):
        super().__init__(name)
        self.__id_vlan = id_vlan
        self.__ip = '127.0.0.1' if ip == 'localhost'else ip

    def check(self, user: UserClient, body: VPNBody) -> bool:
        dest_ip = '127.0.0.1' if body.dest_ip == 'localhost' else body.dest_ip
        return user.id_vlan != self.__id_vlan or dest_ip != self.__ip


class RestrictUser(VPNRule):
    def __init__(self, name, ip, user_id):
        super().__init__(name)
        self.__user_id = user_id
        self.__ip = '127.0.0.1' if ip == 'localhost'else ip

    def check(self, user: UserClient, body: VPNBody) -> bool:
        dest_ip = '127.0.0.1' if body.dest_ip == 'localhost' else body.dest_ip
        return user.id != self.__user_id or dest_ip != self.__ip
