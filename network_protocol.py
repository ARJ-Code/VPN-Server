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
