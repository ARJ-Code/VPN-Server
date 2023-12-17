import os
import json
from vpn_core import VPNBody, UserClient, NetWorkProtocol, VPNRule


class VPN:
    def __init__(self, protocol: NetWorkProtocol) -> None:
        self.__data = VPN.__read_data()
        self.protocol = protocol
        self.rules = []

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
        rule.id = len(self.rules)
        self.rules.append(rule)

        print('Rule added\n')

    def show_rules(self):
        for i in self.rules:
            print(f'Id: {i.id} Name: {i.name}')
        print()

    def remove_rule(self, rule_id: int):
        if rule_id < 0 or rule_id >= len(self.rules):
            print('Rule not found\n')

            return

        new_rules = []
        ind = 0

        for i in self.rules:
            if i.id != rule_id:
                i.id = ind
                ind += 1

                new_rules.append(i)

        self.rules = new_rules

        print('Rule removed\n')

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

        for i in self.rules:
            if not i.check(user, body):
                print(f'Rule {i.name} blocked\n')

                return

        self.protocol.send(body.data, (body.dest_ip, body.dest_port))

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
