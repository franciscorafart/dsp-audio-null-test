import numpy as np
import matplotlib.pyplot as plt
from fractions import gcd
import scipy.fftpack as fftpack
from scipy.signal import find_peaks
# Encoding

# Simple protocol

BASE_FREQ = 2000
fs = 44100
single_char_fft_size = 1024
spread_freq_factor = 10

def max_samples_per_period(freqs, fs):
    return max([int(np.ceil(fs/f)) for f in freqs])

message = 'Hello, this is an audio encoded message'

def ascii_to_freq(code):
    return BASE_FREQ + (code * spread_freq_factor)

def freq_to_ascii(f):
    (f / spread_freq_factor) - BASE_FREQ

# Distance_ is given by the lowest frequency

def encode_message(message):
    freqs = [ascii_to_freq(ord(ch)) for ch in list(message)]
    print('freqs', freqs)
    distance_samples = single_char_fft_size

    buffer = np.zeros(len(freqs)*distance_samples)

    for i, fq in enumerate(freqs):
        left = np.zeros(i*distance_samples)

        n = np.arange(buffer.shape[0] - left.shape[0])
        sine = np.cos(2 * np.pi * fq * n / float(fs))

        if i == len(freqs) - 1:
            right = np.zeros(0)
        else:
            right = np.zeros(buffer.shape[0] - left.shape[0] - sine.shape[0])

        addition_to_buffer = np.concatenate([left, sine, right])

        buffer = buffer + addition_to_buffer

    return buffer

def get_gcd(freqs, fs):
    samples_per_period = [fs/f for f in freqs]
    # print('samples_per_period', samples_per_period)
    accumulator = samples_per_period[0]

    for i in range(1, len(samples_per_period)):
        spp = samples_per_period[i]

        accumulator = accumulator * spp / gcd(accumulator, spp)

    return int(accumulator)


def index_of_largest(numbers):
    max = 0
    idx = 0

    for i, n in enumerate(numbers):
        if abs(n) > max:
            max = n
            idx = i

    return max, idx

def decode(x, distance_samples, fs):
    decoded_freqs = []
    chunk_count = int(x.shape[0] / distance_samples)

    max_freq = np.floor(fs/2) # Nyquist theorem
    frequency_bin_count = distance_samples / 2 # Number of bins = fft size / 2
    freq_range_per_bin = max_freq / frequency_bin_count

    print('chunk count', chunk_count)
    for i in range(0, chunk_count):
        # if i == chunk_count-1:
        #     chunk = x[i*distance_samples:]
        # else:
        chunk = x[i*distance_samples:(i+1)*distance_samples]

        fft = np.real(fftpack.fft(chunk))
        fft_half = fft[:fft.shape[0]//2]
        # plt.plot(fft_half)
        peaks = find_peaks(fft_half)[0]
        # print('possible frews', np.fft.fftfreq(fft_half.shape[0]))
        # _, idx = index_of_largest(fft_half) # NOTE: Likely the problem is here
        idx = max(peaks)

        aprox_freq = idx * freq_range_per_bin
        print('idx', idx, 'freq_range_per_bin', freq_range_per_bin, 'val', fft_half[idx])
        decoded_freqs.append(aprox_freq)

    return decoded_freqs

def snap_frequencies(decoded_freqs, base_frequency):
    idx_closest = 0

    # for i in range (0, 251):

buffer = encode_message('Hello')
print('encode_message', buffer, 'shape', buffer.shape[0])

print('decoded freqs', decode(buffer, single_char_fft_size, fs))

# plt.plot(buffer)
plt.show()
# Sequence of chars
# Get ascii numeric value
# Translate into frequency
# Synthesize sine waves
# write to file

# Decoding
# Get frequency sequence
#


# Decode Real time
