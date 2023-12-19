import os
import json
from vpn_core import VPNBody, UserClient, NetWorkProtocol, VPNRule


class VPN:
    def __init__(self, protocol: NetWorkProtocol) -> None:
        self.__users = VPN.__read_users()
        self.__rules = VPN.__read_rules()
        self.protocol = protocol

    def create_user(self, user: UserClient):
        if any(user.user == i.user for i in self.__users):
            print('User already registered\n')

            return

        user.id = len(self.__users)
        self.__users.append(user)

        self.__save_users()

        print('User registered\n')

    def remove_user(self, user_id: int):
        if user_id < 0 or user_id >= len(self.__users):
            print('User not found\n')

            return

        new_users = []
        ind = 0

        for i in self.__users:
            if i.id != user_id:
                i.id = ind
                ind += 1

                new_users.append(i)

        self.__users = new_users
        self.__save_users()

        print('User removed\n')

    def run(self):
        print('VPN started\n')

        for i in self.protocol.run():
            try:
                body = VPNBody.dict_to_obj(json.loads(i))
                self.__request(body)
            except:
                continue

    def stop(self):
        self.protocol.stop()
        print('VPN stopped\n')

    def add_rule(self, rule: VPNRule):
        if any(rule.name == i.name for i in self.__rules):
            print('There is a rule with that name\n')

            return
        
        rule.id = len(self.__rules)
        self.__rules.append(rule)

        self.__save_rules()

        print('Rule added\n')

    def show_rules(self):
        for i in self.__rules:
            _type = 'VLAN Restriction' if i._type == 0 else 'User Restriction'
            # e_id = f'id_vlan: {i.e_id}' if i._type == 0 else f'user_id: {i.e_id}'
            print(f'Id: {i.id} Name: {i.name} Type: {_type}')
        print()

    def remove_rule(self, rule_id: int):
        if rule_id < 0 or rule_id >= len(self.__rules):
            print('Rule not found\n')

            return

        new_rules = []
        ind = 0

        for i in self.__rules:
            if i.id != rule_id:
                i.id = ind
                ind += 1

                new_rules.append(i)

        self.__rules = new_rules
        self.__save_rules()

        print('Rule removed\n')

    def show_users(self):
        for i in self.__users:
            print(
                f'Id: {i.id} User: {i.user} Password: {i.password} Id_VLAN: {i.id_vlan}')
        print()

    def __request(self, body: VPNBody):
        user = next(
            (i for i in self.__users if i.user == body.user and i.password == body.password), None)

        if user is None:
            print('User not found\n')

            return

        for i in self.__rules:
            if not i.check(user, body):
                print(f'Rule {i.name} blocked\n')

                return

        self.protocol.send(body.data, (body.dest_ip, body.dest_port))

    @staticmethod
    def __read_users():
        path: str = 'data/users.json'

        if not os.path.exists(path):
            return []

        try:
            file = open(path, 'r')
            data = json.load(file)
            file.close()

            return [UserClient.dict_to_obj(i) for i in data]
        except:
            return []

    def __save_users(self):
        path: str = 'data/users.json'

        file = open(path, 'w')
        json.dump(self.__users,  file, default=lambda o: o.__dict__)
        file.close()

    @staticmethod
    def __read_rules():
        path: str = 'data/rules.json'

        if not os.path.exists(path):
            return []

        try:
            file = open(path, 'r')
            data = json.load(file)
            file.close()

            return [VPNRule.dict_to_obj(i) for i in data]
        except:
            return []

    def __save_rules(self):
        path: str = 'data/rules.json'

        file = open(path, 'w')
        json.dump(self.__rules,  file, default=lambda o: {
            'name': o.name,
            'type': o._type,
            'ip': o.ip,
            'e_id': o.e_id
        })
        file.close()
