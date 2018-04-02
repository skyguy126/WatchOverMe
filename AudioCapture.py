import numpy, pyaudio

class AudioCapture:

    def __init__(self, device_number):
        self.device_number = device_number
        self.rate = 44100
        self.buffer_size = 1024
        self.record_time = 1.5

    def setup(self):
        self.num_buffers = int(self.rate * self.record_time / self.buffer_size)
        if self.num_buffers == 0: self.num_buffers = 1
        self.audio = numpy.empty((self.num_buffers * self.buffer_size), dtype=numpy.int16)

        self.p = pyaudio.PyAudio()
        self.input_stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.rate, input=True,
            frames_per_buffer=self.buffer_size, input_device_index=self.device_number)

    # AUDIO

    def get_audio(self):
        audio_string = self.input_stream.read(self.buffer_size)
        return numpy.fromstring(audio_string, dtype=numpy.int16)

    def record(self):
        for i in range(self.num_buffers):
            self.audio[i * self.buffer_size : (i+1) * self.buffer_size] = self.get_audio()
        return self.audio.flatten()
