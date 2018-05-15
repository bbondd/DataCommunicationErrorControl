import socket
import time


class Sender:
    class Constant:
        timeout = 3
        sub_message_size = 0x4
        frame_size = 0x5
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

    def message_to_sub_messages(self, message):
        sub_messages = [message[i: i + self.Constant.sub_message_size]
                        for i in range(0, len(message), self.Constant.sub_message_size)]

        return sub_messages

    def stop_and_wait(self, message):
        sub_messages = self.message_to_sub_messages(message)
        frames = [(sub_messages[i] + chr(i % 2)).encode() for i in range(len(sub_messages))]

        for frame in frames:
            if frame[0] == 'x'.encode()[0]:
                print(frame, ' transmission failed')
            else:
                self.sender.send(frame)
                print(frame, ' transmission completed')

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

    def

def main():
    ip_address = socket.gethostbyname(socket.gethostname())
    port_number = 8585
    sender = Sender(ip_address, port_number)

    while True:
        print('enter message(sub message size : ', sender.Constant.sub_message_size, ') : ')
        message = input()
        print(sender.message_to_sub_messages(message))
        print('send these messages? messages which start with x will fail transmission once.(y/n)')

        if input() == 'y':
            break

    sender.stop_and_wait(message)

    print('send message : ', message)


main()
