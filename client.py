import socket
import pyaudio
from pydub import AudioSegment
import wave
import io
from struct import unpack
from queue import Queue
import threading

END = b""
FORMAT = pyaudio.paInt16
RATE = 44100
SERVER = ('127.0.0.1', 9010)


class AudioSocketWrapper(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)


    def read(self):
        length_bytes = self.recv(4)
        frame_size = unpack('l', length_bytes)[0]
        frame = io.BytesIO(self.recv(frame_size))
        return AudioSegment.from_mp3(frame)


def main():
    with AudioSocketWrapper() as input:
        input.connect(SERVER)
        chunk = input.read()
        play_queue = Queue()
        player_thread = threading.Thread(target=player, args=(play_queue,))
        player_thread.start()
        while chunk != END:
            play_queue.put(chunk.raw_data)
            chunk = input.read()

def player(play_queue):
    p = pyaudio.PyAudio()
    output = p.open(format=FORMAT,
                    channels=1,
                    rate=RATE,
                    output=True)
    while True:
        output.write(play_queue.get())


if __name__ == "__main__":
    main()