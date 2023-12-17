import socket
import struct
from network_protocol import NetWorkProtocol


class TCP(NetWorkProtocol):
    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.__stop = False

    def send(self, data, dest_addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        dest_ip, dest_port = dest_addr
        dest_ip = '127.0.0.1' if dest_ip == 'localhost' else dest_ip

        data = data.encode('utf-8')

        checksum = 0

        tcp_data = struct.pack("!HHLLBBHHH", self._port,
                               dest_port, 0, 0, 52, 2, 0, 0, checksum) + data

        checksum = TCP.__calculate_checksum(self._ip, dest_ip, tcp_data)
        tcp_header = struct.pack('!HHLLBBHHH', self._port,
                                 dest_port, 0, 0, 52, 2, 0, 0, checksum)

        s.sendto(tcp_header + data, (dest_ip, dest_port))

        print(f'TCP data sent to {dest_ip} port {dest_port}\n')
        s.close()

    def run(self):
        self.__stop = False
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        s.bind((self._ip, self._port))
        s.setblocking(False)

        while not self.__stop:
            try:
                data, src_addr = s.recvfrom(1024)
                # print(data)
                p = False

                tcp_header = data[20:40]
                tcp_header = struct.unpack('!HHLLBBHHH', tcp_header)

                src_port = tcp_header[0]
                dest_port = tcp_header[1]
                checksum = tcp_header[8]

                if (dest_port != self._port):
                    continue

                sender_ip, _ = src_addr

                zero_checksum_header = (data[20:40])[:18] + \
                    b'\x00\x00' + (data[20:40])[20:]
                calculated_checksum = TCP.__calculate_checksum(
                    sender_ip, self._ip, zero_checksum_header + data[40:])

                print(f'TCP data received from {sender_ip}')
                print(f'Send from port {src_port} to {dest_port}')

                if checksum != calculated_checksum:
                    print('Corrupted data\n')
                else:
                    data = data[40:].decode('utf-8')
                    print(f'Data: {data}\n')

                    p = True

                if p:
                    yield data
            except:
                continue

    # def send_syn(self, dest_addr):
    #     dest_ip, dest_port = dest_addr
    #     dest_ip = '127.0.0.1' if dest_ip == 'localhost' else dest_ip

    #     syn_flag = 0x02  # SYN flag
    #     control_bits = 0x50  # SYN flag set
    #     seq_num = 0  # Initial sequence number
    #     ack_num = 0  # Initial acknowledgement number
    #     tcp_data = struct.pack(
    #         "!HHLLBBHHH", self._port, dest_port, seq_num, ack_num, 52, control_bits, 0, 0, 0)
    #     checksum = TCP.__calculate_checksum(self._ip, dest_ip, tcp_data)
    #     tcp_header = struct.pack('!HHLLBBHHH', self._port, dest_port,
    #                              seq_num, ack_num, 52, control_bits, 0, 0, checksum)
    #     s.sendto(tcp_header, (dest_ip, dest_port))

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
