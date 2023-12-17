import socket
import struct
from network_protocol import NetWorkProtocol


class UDP(NetWorkProtocol):
    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.__stop = False

    def send(self, data, dest_addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        dest_ip, dest_port = dest_addr
        dest_ip = '127.0.0.1' if dest_ip == 'localhost' else dest_ip

        data = data.encode('utf-8')

        length = 8+len(data)
        checksum = 0

        udp_data = struct.pack("!HHHH", self._port,
                               dest_port, length, checksum) + data

        checksum = UDP.__calculate_checksum(self._ip, dest_ip, udp_data)
        udp_header = struct.pack('!HHHH', self._port,
                                 dest_port, length, checksum)

        s.sendto(udp_header + data, (dest_ip, dest_port))

        print(f'UDP data sent to {dest_ip} port {dest_port}\n')
        s.close()

    def run(self):
        self.__stop = False
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        s.bind((self._ip, self._port))
        s.setblocking(False)

        while not self.__stop:
            try:
                data, src_addr = s.recvfrom(1024)
                p = False

                udp_header = data[20:28]
                udp_header = struct.unpack('!HHHH', udp_header)

                src_port = udp_header[0]
                dest_port = udp_header[1]
                length = udp_header[2]
                checksum = udp_header[3]

                if (dest_port != self._port):
                    continue

                sender_ip, _ = src_addr

                zero_checksum_header = (data[20:28])[:6] + \
                    b'\x00\x00' + (data[20:28])[8:]
                calculated_checksum = UDP.__calculate_checksum(
                    sender_ip, self._ip, zero_checksum_header + data[28:])

                print(f'UDP data received from {sender_ip}')
                print(f'Send from port {src_port} to {dest_port}')

                if checksum != calculated_checksum:
                    print('Corrupted data\n')
                else:
                    data = data[28:].decode('utf-8')
                    print(f'Data: {data}')
                    print(f'Length: {length}, Checksum: {checksum}\n')

                    p = True

                if p:
                    yield data
            except BlockingIOError:
                continue

    def stop(self):
        self.__stop = True

    @staticmethod
    def __calculate_checksum(source_ip, dest_ip, data):
        source_ip = socket.inet_aton(source_ip)
        dest_ip = socket.inet_aton(dest_ip)

        packet = struct.pack('!4s4sHH', source_ip,
                             dest_ip, len(data), 0) + data

        checksum = 0
        for i in range(0, len(packet), 2):
            if i + 1 < len(packet):
                checksum += (packet[i] << 8) + packet[i+1]
            else:
                checksum += packet[i]
            while checksum >> 16:
                checksum = (checksum & 0xFFFF) + (checksum >> 16)

        checksum = ~checksum

        return checksum & 0xFFFF
