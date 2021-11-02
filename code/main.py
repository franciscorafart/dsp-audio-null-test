import numpy as np
from audio_utils import read_audio_file, play_audio_file, write_audio_file, shift_phase, spectrum
from effects import apply_pedal

import matplotlib.pyplot as plt

# TODO: extract from command line
filename = 'audio/singing-female.wav'
processed_filename = 'audio/processed.wav'
null_test_filename = 'audio/null-test.wav'

# Original signal, processed signal, and null test signal
fs, x = read_audio_file(filename)
processed_x = apply_pedal(x, fs)
x_shifted = shift_phase(x, np.pi) # Phase shifting x by 180 degrees (π)

min_samples = min(x_shifted.shape[0], processed_x.shape[0])
# Combine the two signals to extract pure effect
null_test_signal = processed_x[0:min_samples] + x_shifted[0:min_samples]



# Plot
fig, ((x1, k1), (x2, k2), (x3, k3)) = plt.subplots(3, 2)

t = np.arange(0, min_samples, 100)
fig.suptitle('Signals')

x1.set_ylim([-1,1])
x2.set_ylim([-1,1])
x3.set_ylim([-1,1])

x1.plot(x, label='original signal')
x2.plot(processed_x, color='g', label='processed signal') 
x3.plot(null_test_signal, color='r', label='null test')

# TODO: Plot spectrums with logarithmic scale
k1.plot(spectrum(x))
k2.plot(spectrum(processed_x), color='g')
k3.plot(spectrum(null_test_signal), color='r')

plt.show()

write_audio_file(null_test_signal, fs, null_test_filename)
write_audio_file(processed_x, fs, processed_filename)

play_audio_file(null_test_filename)

