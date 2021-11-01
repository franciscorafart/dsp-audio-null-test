from audio_utils import read_audio_file 

fs, x = read_audio_file('audio/singing-female.wav')

print('sample rate', fs)
print('signal', x)
