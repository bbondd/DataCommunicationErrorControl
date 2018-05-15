import socket


class Receiver:
    class Constant:
        sub_message_size = 0x4
        frame_size = 0x5

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

    def stop_and_wait(self, successes_and_fails):
        message = ''

        previous_acknowledgement = 1
        for i in range(len(successes_and_fails)):
            frame = self.receiver.recv(self.Constant.frame_size)
            if frame[-1] != previous_acknowledgement:
                message += frame[0:-1].decode()
                previous_acknowledgement = not previous_acknowledgement

            if successes_and_fails[i] == 'o':
                self.receiver.send('\0'.encode())
                print('acknowledgement transmission completed')
            else:
                print('acknowledgement transmission failed')

        return message


def main():
    ip_address = socket.gethostbyname(socket.gethostname())
    port_number = 8585
    receiver = Receiver(ip_address, port_number)

    print('enter acknowledgement transmission success or fail (ex : oxoox): ')
    message = receiver.stop_and_wait(input())

    print('received message : ', message)


main()
