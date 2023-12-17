import socket
import struct
from network_protocol import NetWorkProtocol

FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
MAX_COUNT = 1000


class TCP(NetWorkProtocol):
    def __init__(self, ip, port):
        super().__init__(ip, port)
        self.__stop = False

    def send(self, data, dest_addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        dest_ip, dest_port = dest_addr
        dest_ip = '127.0.0.1' if dest_ip == 'localhost' else dest_ip

        s.bind((self._ip, self._port))
        s.setblocking(False)

        handshake, client_seq, client_ack = self.__handshake_client(
            dest_ip, dest_port, s)

        if not handshake:
            print('TCP connection error\n')

            return

        print('TCP connection established')

        send_package = self.__send_package(
            s, dest_ip, dest_port, client_seq, client_ack, data)

        if not send_package:
            print('TCP connection error\n')

            return

        print(f'TCP data sent to {dest_ip} port {dest_port}')

        self.__finished_client(s, dest_ip, dest_port, client_seq, client_ack)
        print('TCP connection finished\n')

        s.close()

    def run(self):
        self.__stop = False
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                          socket.IPPROTO_TCP)
        s.bind((self._ip, self._port))
        s.setblocking(False)

        while not self.__stop:
            p, data = self.__new_connection(s)

            if p:
                yield data

    def __new_connection(self, s):
        handshake, src_ip_c, src_port_c, server_seq, server_ack = self.__handshake_server(
            s)

        if not handshake:
            return (False, '')

        print('TCP connection established')

        package, data = self.__received_package(
            s, src_ip_c, src_port_c, server_seq, server_ack)

        if not package:
            print('TCP connection error\n')

            return (False, '')

        print(f'Data: {data}')

        fin = self.__finished_server(
            s, src_ip_c, src_port_c, server_seq, server_ack)

        if fin:
            print('TCP connection finished\n')
        else:
            print('TCP connection error\n')

        return (True, data)

    def __handshake_client(self, dest_ip, dest_port, s):
        client_seq = 0
        client_ack = 0

        syn_data = self.__build_package(
            dest_ip, dest_port, client_seq, client_ack, (5 << 12) | SYN)

        s.sendto(syn_data, (dest_ip, dest_port))

        syn_ack, _, _, seq_s, ack_s, _ = self.__listening(
            s, lambda flags: flags & SYN and flags & ACK, dest_ip, dest_port, client_seq, client_ack)

        if not syn_ack:
            return (False, 0, 0)

        client_seq = ack_s
        client_ack = seq_s+1

        ack_data = self.__build_package(
            dest_ip, dest_port, client_seq, client_ack, (5 << 12) | ACK)

        s.sendto(ack_data, (dest_ip, dest_port))

        return (True, client_seq, client_ack)

    def __send_package(self, s, dest_ip, dest_port, client_seq, client_ack, data):
        ind = 0

        while True:
            if (ind == MAX_COUNT):
                return False
            ind += 1

            package = self.__build_package(
                dest_ip, dest_port, client_seq, client_ack, (5 << 12), data)
            s.sendto(package, (dest_ip, dest_port))

            ack, _, _, seq_s, ack_s, _ = self.__listening(
                s, lambda flags:  flags & ACK, dest_ip, dest_port, client_seq, client_ack)

            if seq_s == -1 or ack_s == -1:
                return False

            client_seq = ack_s
            client_ack = seq_s+1

            if ack:
                return True

    def __finished_client(self, s, dest_ip, dest_port, client_seq, client_ack):
        fin_data = self.__build_package(
            dest_ip, dest_port, client_seq, client_ack, (5 << 12) | FIN, '')
        s.sendto(fin_data, (dest_ip, dest_port))

    def __handshake_server(self, s):
        syn, src_ip_c, src_port_c, seq_s, ack_s, _ = self.__listening(
            s, lambda flags: flags & SYN)

        if not syn:
            return (False, 0, 0, 0, 0)

        server_seq = ack_s
        server_ack = seq_s+1

        syn_ack_data = self.__build_package(
            src_ip_c, src_port_c, server_seq, server_ack, (5 << 12) | SYN | ACK)

        s.sendto(syn_ack_data, (src_ip_c, src_port_c))

        ack, _, _, seq_s, ack_s, _ = self.__listening(
            s, lambda flags: flags & ACK, src_ip_c, src_port_c, server_seq, server_ack)

        if not ack:
            return (False, 0, 0, 0, 0)

        return (True, src_ip_c, src_port_c, server_seq, server_ack)

    def __received_package(self, s, src_ip, src_port, server_seq, server_ack):
        ind = 0

        while True:
            if (ind == MAX_COUNT):
                return (False, '')
            ind += 1

            package, _, _, seq_c, ack_c, data = self.__listening(
                s, lambda _:  True, src_port, server_seq, server_ack)

            if seq_c == -1 or ack_c == -1:
                return (False, '')

            server_seq = ack_c
            server_ack = seq_c+1

            if package:
                ack_data = self.__build_package(
                    src_ip, src_port, server_seq, server_ack, (5 << 12) | ACK)
                s.sendto(ack_data, (src_ip, src_port))

                return (True, data)

            ack_data = self.__build_package(
                src_ip, src_port, server_seq, server_ack, (5 << 12))
            s.sendto(ack_data, (src_ip, src_port))

    def __finished_server(self, s, src_ip, src_port, server_seq, server_ack):
        fin, _, _, _, _, _ = self.__listening(
            s, lambda flags: flags & FIN, src_ip, src_port, server_seq, server_ack)
        return fin

    def __listening(self, s, check_flags, request_ip='-1', request_port=-1, request_seq=-1, request_ack=-1):
        preview = request_ip != '-1' and request_port != - \
            1 and request_seq != -1 and request_ack != -1

        ind = 0
        while True:
            if ind == MAX_COUNT:
                return (False, -1, -1, -1, -1, '')
            ind += 1

            try:
                data, src_addr = s.recvfrom(1024)

                src_port_r, dest_port_r, seq_r, ack_r, flags_r, checksum_r = self.__decode_package(
                    data)

                if preview:
                    if dest_port_r != self._port or request_port != src_port_r:
                        continue
                else:
                    if dest_port_r != self._port:
                        continue

                sender_ip, _ = src_addr

                if preview and sender_ip != request_ip:
                    continue

                if not self.__check_package(sender_ip, checksum_r, data):
                    continue

                if preview:
                    if request_ack == seq_r and request_seq+1 == ack_r:
                        return (check_flags(flags_r), sender_ip, src_port_r, seq_r, ack_r, data[40:].decode('utf-8'))
                else:
                    if check_flags(flags_r):
                        return (check_flags(flags_r), sender_ip, src_port_r, seq_r, ack_r, data[40:].decode('utf-8'))

            except BlockingIOError:
                continue

    def __build_package(self,  dest_ip, dest_port, seq, ack, flags, data=''):
        data = data.encode('utf-8')

        checksum = 0
        tcp_data = struct.pack("!HHLLBBHHH", self._port,
                               dest_port, seq, ack, 52, 2, flags, 0, checksum) + data

        checksum = TCP.__calculate_checksum(self._ip, dest_ip, tcp_data)
        tcp_header = struct.pack("!HHLLBBHHH", self._port,
                                 dest_port, seq, ack, 52, 2, flags, 0, checksum)

        return tcp_header+data

    def __decode_package(self, data):
        tcp_header = data[20:40]
        tcp_header = struct.unpack('!HHLLBBHHH', tcp_header)

        src_port = tcp_header[0]
        dest_port = tcp_header[1]
        seq = tcp_header[2]
        ack = tcp_header[3]
        flags = tcp_header[6]
        checksum = tcp_header[8]

        return (src_port, dest_port, seq, ack, flags, checksum)

    def __check_package(self, sender_ip, checksum, data):
        zero_checksum_header = (data[20:40])[:18] + \
            b'\x00\x00' + (data[20:40])[20:]
        calculated_checksum = TCP.__calculate_checksum(
            sender_ip, self._ip, zero_checksum_header + data[40:])

        return checksum == calculated_checksum

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
