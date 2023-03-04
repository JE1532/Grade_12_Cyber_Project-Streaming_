import tempfile
import socket
from pydub import AudioSegment
import time
import math
import io
import glob
import sys
import os
from struct import pack

CHUNK_SIZE = 1024
SERVER = ('0.0.0.0', 9010)
END = b"__stream-end__"
FREQUENCY_BITS_TO_VALUE = {0 : 22050, 1 : 24000, 2 : 16000}
BITRATE_BITS_TO_VALUE = lambda bits : 32 * bits
RESOURCE_PATH = os.path.dirname(sys.argv[0]) + '/resc.mp3'
#AudioSegment.converter = r'C:\stuff\ffmpeg-6.0-full_build-shared\bin'

class ChunkIterator:
    def __init__(self, audio, chunk_time):
        self.audio = audio
        self.chunk_time = chunk_time
        self.curr_time = 0
        self.audio_length = math.ceil(len(self.audio) / 1000)

    def has_next_chunk(self):
        return self.curr_time < self.audio_length

    def next_chunk(self):
        chunk_end = self.chunk_time * 1000 + self.curr_time * 1000
        chunk_start = self.curr_time * 1000
        chunk = self.audio[chunk_start:chunk_end]
        chunk.export('test.mp3', 'mp3')
        self.curr_time = chunk_end / 1000
        chunk_mp3 = ChunkIterator.to_mp3(chunk)
        return chunk_mp3

    @staticmethod
    def to_mp3(chunk):
        chunk.export(RESOURCE_PATH, format='mp3')
        with open(RESOURCE_PATH, 'rb') as resource:
            chunk_mp3 = resource.read()
        return chunk_mp3




def stream_mp3_audio(audio, output):
    print('File open succeeded.')
    chunk_iterator = ChunkIterator(audio, 1)
    while chunk_iterator.has_next_chunk():
        chunk = chunk_iterator.next_chunk()
        data = pack('l', len(chunk)) + chunk
        output.send(bytes(data))
    print('Finished Streaming.')


def main():
    ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ser_sock.bind(SERVER)
    ser_sock.listen(1)
    print('Server ready.')
    cli_sock, cli_addr = ser_sock.accept()
    print('Client connected. Streaming audio.')
    wav_file = AudioSegment.from_wav(file="longSoundExample.wav")
    stream_mp3_audio(wav_file, cli_sock)





if __name__ == "__main__":
    main()