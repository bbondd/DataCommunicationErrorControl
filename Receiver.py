import socket


class Receiver:
    class Constant:
        frame_size = 0x10
        acknowledgement = 'ACK'.encode()

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

    def stop_and_wait(self):
        frame = self.receiver.recv(self.Constant.frame_size)
        print('data reception completed')
        self.receiver.send(self.Constant.acknowledgement)
        print('acknowledgement transmission completed')

        return frame


def main():
    ip_address = socket.gethostbyname(socket.gethostname())
    port_number = 8585

    receiver = Receiver(ip_address, port_number)
    frame = receiver.stop_and_wait()

    print('received frame : ', frame)


main()
