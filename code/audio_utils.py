import os, sys
from sys import platform
import subprocess

from scipy.io.wavfile import read, write

# NOTE: Code copied from ...

def read_audio_file(file):
    if (os.path.isfile(file) == False):
        raise ValueError('{} is not a file'.format(file))
    
    sample_rate, signal = read(file)

    return sample_rate, signal

def play_audio_file(file):
    if (os.path.isfile(file) == False):
        raise ValueError('{} is not a file'.format(file))

    # OSX
    if sys.platform == 'darwin':
        subprocess.call(['afplay', file])
    else:
        print('Not a recognized platform')
    

