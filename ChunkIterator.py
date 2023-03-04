import math

class ChunkIterator:
    def __init__(self, audio, chunk_time, tempfile_path):
        self.audio = audio
        self.chunk_time = chunk_time
        self.curr_time = 0
        self.audio_length = math.ceil(len(self.audio) / 1000)
        self.tempfile = tempfile_path

    def has_next_chunk(self):
        return self.curr_time < self.audio_length

    def next_chunk(self):
        chunk_end = self.chunk_time * 1000 + self.curr_time * 1000
        chunk_start = self.curr_time * 1000
        chunk = self.audio[chunk_start:chunk_end]
        chunk.export('test.mp3', 'mp3')
        self.curr_time = chunk_end / 1000
        chunk_mp3 = ChunkIterator.to_mp3(chunk, self.tempfile)
        return chunk_mp3

    @staticmethod
    def to_mp3(chunk, tempfile):
        chunk.export(tempfile, format='mp3')
        with open(tempfile, 'rb') as resource:
            chunk_mp3 = resource.read()
        return chunk_mp3