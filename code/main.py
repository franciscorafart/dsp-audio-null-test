from audio_utils import read_audio_file, play_audio_file 

# TODO: extract from command line
filename = 'audio/singing-female.wav'

fs, x = read_audio_file(filename)

print('sample rate', fs)
print('signal', x)

play_audio_file(filename)
