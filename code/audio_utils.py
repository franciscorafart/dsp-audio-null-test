import copy, os, sys
import numpy as np
import subprocess
import cmath
import scipy.fftpack as fftpack

from scipy.io.wavfile import read, write

INT16_FAC = (2**15)-1
INT32_FAC = (2**31)-1
INT64_FAC = (2**63)-1
norm_fact = {'int16':INT16_FAC, 'int32':INT32_FAC, 'int64':INT64_FAC,'float32':1.0,'float64':1.0}

# NOTE: Code copied from ...

def read_audio_file(file):
    if (os.path.isfile(file) == False):
        raise ValueError('{} is not a file'.format(file))
    
    sample_rate, signal = read(file)

	# NOTE: Important: Understand this normalization  1
    #scale down and convert audio into floating point number in range of -1 to 1
    x = np.float32(signal)/norm_fact[signal.dtype.name]

    return sample_rate, x

def play_audio_file(file):
    if (os.path.isfile(file) == False):
        raise ValueError('{} is not a file'.format(file))

    # OSX
    if sys.platform == 'darwin':
        subprocess.call(['afplay', file])
    else:
        print('Not a recognized platform')

def write_audio_file(y, sample_rate, filename):
    x = copy.deepcopy(y)
    x *= INT16_FAC
    x = np.int16(x)
    write(filename, sample_rate, x)


#### 

# Reference: https://stackoverflow.com/questions/52179919/amplitude-and-phase-spectrum-shifting-the-phase-leaving-amplitude-untouched
def shift_phase(x, radians):
    xFFT = fftpack.rfft(x)
    xFFT_phase_shift = np.real(xFFT * cmath.rect( 1., radians))
    x_shifted = fftpack.irfft(xFFT_phase_shift)

    return x_shifted

def spectrum(x):
    return fftpack.rfft(x)


