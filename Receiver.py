import socket


class Receiver:
    class Constant:
        sub_message_size = 0x4
        frame_size = 0x5
        window_size = 4

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

    def stop_and_wait(self, do_transmissions):
        message = ''

        previous_acknowledgement = 1
        for do_transmission in do_transmissions:
            frame = self.receiver.recv(self.Constant.frame_size)

            if len(frame) == 0:
                return message

            if frame[-1] != previous_acknowledgement:
                message += frame[0:-1].decode()
                previous_acknowledgement = not previous_acknowledgement

            if do_transmission:
                self.receiver.send(chr(0).encode())
                print('acknowledgement transmission completed')
            else:
                print('acknowledgement transmission failed')

        return message

    def go_back_n(self, do_transmissions):
        message = ''

        next_frame_number = 0
        for do_transmission in do_transmissions:
            for _ in range(self.Constant.window_size):

                try:
                    frame = self.receiver.recv(self.Constant.frame_size)
                except ConnectionAbortedError:
                    return message

                if len(frame) == 0:
                    continue

                if frame[-1] == next_frame_number:
                    message += frame[0:-1].decode()
                    next_frame_number += 1

            if do_transmission:
                self.receiver.send(chr(next_frame_number).encode())
                print('acknowledgement transmission completed')
            else:
                print('acknowledgement transmission failed')

        return message


def main():
    ip_address = socket.gethostbyname(socket.gethostname())
    port_number = 8585
    receiver = Receiver(ip_address, port_number)

    print('1. stop and wait')
    print('2. go back n')
    print('choose method : ')
    method = int(input())

    print('enter acknowledgement transmission success or fail using o and x (ex : oxoox): ')

    

    message = receiver.go_back_n([True if character == 'o' else False for character in input()])




    print('received message : ', message)


main()
