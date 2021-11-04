from audio_utils import play_audio_file
from main import process_file
from tkinter import filedialog

class AudioContext():
    def __init__(self):
        self.original_filename = None
        self.processed_filename = None
        self.null_test_filename = None

    # Move to its own folder
    def import_click(self):
        self.original_filename = filedialog.askopenfilename(filetypes = (("Wav files","*.wav"),("all files","*.*")))
        null, processed = process_file(self.original_filename)

        self.null_test_filename = null
        self.processed_filename = processed

    def play_null(self):
        play_audio_file(self.null_test_filename)

    def play_processed(self):
        play_audio_file(self.processed_filename)

    def play_original(self):
        play_audio_file(self.original_filename)