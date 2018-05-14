import socket
import time
import random
import string


class Sender:
    class Constant:
        timeout = 3
        message_size = 0x4
        frame_size = message_size + 1
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

        sender.settimeout(self.Constant.timeout)
        print('connection completed')

        return sender

    def __init__(self, ip_address, port_number):
        self.sender = self.make_connection(ip_address, port_number)

    def stop_and_wait(self, message):

        for i in range():

        while index < len(message):
            sub_message = message[index: index + self.Constant.frame_size - 1]
            frame = (sub_message + chr())

            sub_message = message[start_index: start_index + self.Constant.frame_size - 1]
            frame = (sub_message + chr(acknowledgement)).encode()

            print(frame)
            print('send this frame?(y/n)')

            if input() == 'y':
                self.sender.send(frame)
                print('frame transmission completed')

            else:
                print('frame transmission failed')

            while True:
                try:
                    self.sender.recv(self.Constant.frame_size)
                    print('received acknowledgement')
                    break

                except socket.timeout:
                    print('acknowledgement reception failed')
                    print('retransmitting...')
                    self.sender.send(frame)
                    print('frame transmission completed')

            return message + recursive_stop_and_wait(remain_frame_number - 1, not acknowledgement)

        return recursive_stop_and_wait(frame_number, 0)


def main():
    ip_address = socket.gethostbyname(socket.gethostname())
    port_number = 8585
    sender = Sender(ip_address, port_number)

    print('enter message : ')
    message = input()

    sender.stop_and_wait(message)

    print('send message : ', message)


main()
