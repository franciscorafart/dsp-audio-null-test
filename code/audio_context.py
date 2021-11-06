import numpy as np
from audio_utils import play_audio_file, write_audio_file, shift_phase,read_audio_file
from tkinter import filedialog
from effects import apply_pedal

processed_filename = 'audio/processed.wav'
null_test_filename = 'audio/null-test.wav'

def process_file(filename):
    # Original signal, processed signal, and null test signal
    fs, signal = read_audio_file(filename)
    processed_signal = apply_pedal(signal, fs)
    x_shifted = shift_phase(signal, np.pi) # Phase shifting x by 180 degrees (π)

    min_samples = min(x_shifted.shape[0], processed_signal.shape[0])
    # Combine the two signals to extract pure effect
    null_signal = processed_signal[0:min_samples] + x_shifted[0:min_samples]

    write_audio_file(null_signal, fs, null_test_filename)
    write_audio_file(processed_signal, fs, processed_filename)

    return signal, processed_signal, null_signal, min_samples, fs

class AudioContext():
    def __init__(self):
        self.original_filename = None
        self.processed_filename = processed_filename
        self.null_filename = null_test_filename

    def import_click(self):
        self.original_filename = filedialog.askopenfilename(filetypes = (("Wav files","*.wav"),("all files","*.*")))
        signal, processed_signal, null_signal, min_samples, fs = process_file(self.original_filename)

        return signal, processed_signal, null_signal, min_samples, fs

    def play_null(self):
        play_audio_file(self.null_filename)

    def play_processed(self):
        play_audio_file(self.processed_filename)

    def play_original(self):
        play_audio_file(self.original_filename)