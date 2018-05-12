import socket
import time
import random
import string


class Sender:
    class Constant:
        timeout = 2
        frame_size = 0x10
        frame_transmission_failure_probability = 0.3
        reconnect_wait_time = 1  # sec

    def make_connection(self, ip_address, port_number):
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sender.connect((ip_address, port_number))

        except ConnectionRefusedError:
            print('connection failed')
            print('reconnecting...')
            time.sleep(self.Constant.reconnect_wait_time)
            return self.make_connection(ip_address, port_number)

        print('connection completed')
        sender.settimeout(self.Constant.timeout)

        return sender

    def __init__(self, ip_address, port_number):
        self.sender = self.make_connection(ip_address, port_number)

    def stop_and_wait(self, frame):
        if random.random() < self.Constant.frame_transmission_failure_probability:
            print('frame transmission failed')
        else:
            self.sender.send(frame)
            print('frame transmission completed')

        try:
            self.sender.recv(self.Constant.frame_size)

        except socket.timeout:
            print('acknowledgement reception failed')
            print('retransmitting...')
            return self.stop_and_wait(frame)

        print('acknowledgement reception completed')
        return frame

    def make_random_frame(self):
        return ''.join(random.choice(string.ascii_uppercase) for _ in range(self.Constant.frame_size)).encode()


def main():
    ip_address = socket.gethostbyname(socket.gethostname())
    port_number = 8585

    sender = Sender(ip_address, port_number)
    sender.stop_and_wait(sender.make_random_frame())


main()
