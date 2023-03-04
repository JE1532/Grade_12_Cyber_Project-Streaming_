from ChunkIterator import ChunkIterator
from pydub import AudioSegment

END = b'__end__'

class StreamerReceiver:
    def __init__(self, audio_path, tempfile_path, chunk_time, audio_send_queue):
        self.audio = AudioSegment.from_wav(audio_path)
        self.chunk_iterator = ChunkIterator(self.audio, chunk_time, tempfile_path)
        self.audio_send_queue = audio_send_queue
        self.start()


    def start(self):
        while self.chunk_iterator.has_next_chunk():
            self.audio_send_queue.put(self.chunk_iterator.next_chunk())
        self.audio_send_queue.put(END)
