from queue import Queue
from Streamer_Sender import StreamerSender
from Streamer_Receiver import StreamerReceiver
import threading

class Streamer:
    def __init__(self, tempfile_path, audio_path, client_socket, chunk_time):
        self.tempfile_path = tempfile_path
        self.send_queue = Queue()
        self.receiver_thread = threading.Thread(target=StreamerReceiver, args=(audio_path, tempfile_path, chunk_time, self.send_queue))
        self.sender_thread = threading.Thread(target=StreamerSender, args=(client_socket, self.send_queue))
        self.start()


    def start(self):
        self.receiver_thread.start()
        self.sender_thread.start()
