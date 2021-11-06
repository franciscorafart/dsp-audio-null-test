import numpy as np
from audio_utils import play_audio_file, spectrum, write_audio_file, shift_phase,read_audio_file
from tkinter import filedialog
from effects import apply_pedal

processed_filename = 'audio/processed.wav'
null_test_filename = 'audio/null-test.wav'

def process_file(filename):
    fs, signal = read_audio_file(filename)
    processed_signal = apply_pedal(signal, fs)
    null_signal = processed_signal - signal

    write_audio_file(null_signal, fs, null_test_filename)
    write_audio_file(processed_signal, fs, processed_filename)

    return signal, processed_signal, null_signal, fs

class AudioContext():
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

    def import_click(self):
        self.original_filename = filedialog.askopenfilename(filetypes = (("Wav files","*.wav"),("all files","*.*")))
        signal, processed_signal, null_signal, fs = process_file(self.original_filename)
       
        self.signal = signal
        self.signal_spectrum = spectrum(signal)

        self.processed_signal = processed_signal
        self.processed_spectrum = spectrum(processed_signal)

        self.null_signal = null_signal
        self.null_spectrum = spectrum(null_signal)

        self.sample_rate = fs

    def play_null(self):
        play_audio_file(self.null_filename)

    def play_processed(self):
        play_audio_file(self.processed_filename)

    def play_original(self):
        play_audio_file(self.original_filename)