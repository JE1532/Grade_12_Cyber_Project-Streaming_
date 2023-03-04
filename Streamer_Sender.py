import socket
from struct import pack

END = b'__end__'

class StreamerSender:
    def __init__(self, client_socket, send_queue):
        self.send_queue = send_queue
        self.client_socket = client_socket
        self.start()

    def start(self):
        curr_chunk = self.send_queue.get()
        while curr_chunk != END:
            self.client_socket.send(pack('l', len(curr_chunk)) + curr_chunk)
            curr_chunk = self.send_queue.get()
