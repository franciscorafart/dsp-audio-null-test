import os
from sys import platform
import subprocess

from scipy.io.wavfile import read, write

def read_audio_file(file):
    if (os.path.isfile(file) == False):
        raise ValueError('{} is not a file'.format(file))
    
    sample_rate, signal = read(file)

    return sample_rate, signal

# def play_audio_file(file):
#     if platform
