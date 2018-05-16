import socket
import time


class Sender:
    class Constant:
        timeout = 3
        sub_message_size = 4
        frame_size = 5
        reconnect_wait_time = 1  # sec
        window_size = 4

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

    def message_to_sub_messages(self, message):
        sub_messages = [message[i: i + self.Constant.sub_message_size]
                        for i in range(0, len(message), self.Constant.sub_message_size)]

        return sub_messages

    def stop_and_wait(self, message):
        sub_messages = self.message_to_sub_messages(message)
        frames = [(sub_messages[i] + chr(i % 2)).encode() for i in range(len(sub_messages))]

        for frame in frames:
            if frame[0] == ord('x'):
                print(frame[0:-1].decode(), 'transmission failed')
            else:
                self.sender.send(frame)
                print(frame[0:-1].decode(), 'transmission completed')

            while True:
                try:
                    self.sender.recv(self.Constant.frame_size)
                    print('received acknowledgement')
                    break

                except socket.timeout:
                    print('acknowledgement reception failed')
                    print('retransmitting...')
                    self.sender.send(frame)
                    print(frame[0:-1].decode(), 'transmission completed')

                except ConnectionResetError:
                    return message

    def go_back_n(self, message):
        sub_messages = self.message_to_sub_messages(message)
        frames = [(sub_messages[i] + chr(i)).encode() for i in range(len(sub_messages))]

        window_start_index = 0
        already_failed = [False for _ in range(len(frames))]

        while window_start_index < len(frames):
            for i in range(window_start_index, window_start_index + self.Constant.window_size):
                try:
                    if frames[i][0] == ord('x') and not already_failed[i]:
                        print(frames[i][0:-1].decode(), 'transmission failed')
                        already_failed[i] = True
                    else:
                        self.sender.send(frames[i])
                        print(frames[i][0:-1].decode(), 'transmission completed')

                except IndexError:
                    break

            try:
                window_start_index = ord(self.sender.recv(self.Constant.frame_size))
                print('received acknowledgement')

            except socket.timeout:
                print('acknowledgement reception failed')
                print('retransmitting...')


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

    sender.go_back_n(message)

    print('sent message : ', message)


main()
