import numpy as np
from audio_utils import read_audio_file, play_audio_file
import soundfile as sf
from effects import apply_pedal

import matplotlib.pyplot as plt

# TODO: extract from command line
filename = 'audio/singing-female.wav'
new_filename = 'audio/processed.wav'

fs, x = read_audio_file(filename)

print('signal length:', x.shape[0], 'sample rate:', fs)

processed_audio = apply_pedal(x, fs)

# Plot
# TODO: Figure out how to plot 2 signals
# plt.plot(x)
# plt.plot(processed_audio)
# plt.axis([0, 0, 0, ])
# plt.show()


# TODO: Implememt writing function 
with sf.SoundFile(new_filename, 'w', samplerate=fs, channels=len(processed_audio.shape)) as f:
    f.write(processed_audio)

play_audio_file(new_filename)

