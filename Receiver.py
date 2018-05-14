import socket


class Receiver:
    class Constant:
        frame_size = 0x100

    def make_connection(self, ip_address, port_number):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip_address, port_number))
        server.listen(0)

        print('waiting connection...')
        receiver = server.accept()[0]
        print('connection completed')

        return receiver

    def __init__(self, ip_address, port_number):
        self.receiver = self.make_connection(ip_address, port_number)

    def stop_and_wait(self, frame_number):
        def recursive_stop_and_wait(remain_frame_number, acknowledgement):
            if remain_frame_number == 0:
                return ''

            frame = self.receiver.recv(self.Constant.frame_size)
            message = frame.decode()[0:-1]

            print('data reception completed')
            print(message, '\treceived')

            print('send acknowledgement?(y/n)')

            if input() == 'y':
                self.receiver.send(chr(not acknowledgement).encode())
                print('acknowledgement transmission completed')

            else:
                print('acknowledgement transmission failed')

            if frame[-1] == acknowledgement:
                return message + recursive_stop_and_wait(remain_frame_number - 1, not acknowledgement)
            else:
                return recursive_stop_and_wait(remain_frame_number, not acknowledgement)

        return recursive_stop_and_wait(frame_number, 0)


def main():
    ip_address = socket.gethostbyname(socket.gethostname())
    port_number = 8585
    receiver = Receiver(ip_address, port_number)

    print('enter frame number : ')
    message = receiver.stop_and_wait(int(input()))

    print('received message : ', message)


main()
