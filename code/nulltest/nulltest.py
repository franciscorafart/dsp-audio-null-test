import numpy as np
from audio_utils import play_audio_file, spectrum, write_audio_file, read_audio_file

processed_filename = 'audio/processed.wav'
null_test_filename = 'audio/null-test.wav'

def _process_file(filename, pedal):
    fs, signal = read_audio_file(filename)
    processed_signal = pedal.process_signal_chain(signal, fs)
    null_signal = processed_signal - signal

    write_audio_file(null_signal, fs, null_test_filename)
    write_audio_file(processed_signal, fs, processed_filename)

    return signal, processed_signal, null_signal, fs

class NullTest():
    def __init__(self):
        self.original_filename = None
        self.processed_filename = processed_filename
        self.null_filename = null_test_filename

        self.signal = None
        self.processed_signal = None
        self.null_signal = None

        self.signal_spectrum = None
        self.processed_spectrum = None
        self.null_spectrum = None

        self.sample_rate = None

    def process(self, pedal, filename):
        self.original_filename = filename
        signal, processed_signal, null_signal, fs = _process_file(self.original_filename, pedal)

        self.signal = signal
        self.signal_spectrum = spectrum(signal)

        self.processed_signal = processed_signal
        self.processed_spectrum = spectrum(processed_signal)

        self.null_signal = null_signal
        self.null_spectrum = spectrum(null_signal)

        self.sample_rate = fs

    def play(self, identifier):
        if identifier == 'original':
            play_audio_file(self.null_filename)
        elif identifier == 'processed':
            play_audio_file(self.processed_filename)
        elif identifier == 'null':
            play_audio_file(self.original_filename)

