import numpy as np
from audio_utils import spectrum, complex_spectrum, read_audio_file, write_audio_file
import scipy.fftpack as fftpack

class Convolve():
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def set_real_spectrum(self, gain_factor=0.1):
        x_pad, y_pad = self._zero_pad(gain_factor)
        self.spectrum_y = spectrum(y_pad)
        self.spectrum_x = spectrum(x_pad)

    def set_complex_spectrum(self, gain_factor=0.1):
        x_pad, y_pad = self._zero_pad(gain_factor)
        self.spectrum_y = complex_spectrum(y_pad)
        self.spectrum_x = complex_spectrum(x_pad)

    # NOTE: Doing convolution by doing fft -> multiplying the frequency domains -> doing inverse fft. O(n log(n))
    def convolve_freq_complex(self):
        self.set_complex_spectrum()
        convolution = self.spectrum_y * self.spectrum_x

        return fftpack.ifft(convolution)

    # NOTE: Doing convolution by doing fft -> multiplying the frequency domains -> doing inverse fft. O(n log(n))
    # Doing it only in the real spectrum (cuts the audio duration)
    def convolve_freq_real(self):
        self.set_real_spectrum()

        convolution = self.spectrum_y * self.spectrum_x

        return fftpack.irfft(convolution)

    # NOTE: Direct convolution in the time domain - O(N^2)
    def convolve_time_domain(self, gain_factor=0.1):
        max_length = max(self.x.shape[0], self.y.shape[0])
        x_pad = np.concatenate([self.x, np.repeat(0, int(max_length-self.x.shape[0]))]) * gain_factor
        y_pad = np.concatenate([self.y, np.repeat(0, int(max_length-self.y.shape[0]))]) * gain_factor

        return np.convolve(x_pad, y_pad)

    def _zero_pad(self, gain_factor=0.1):
        max_length = self.x.shape[0] + self.y.shape[0] - 1
        # max_length = max(self.x.shape[0], self.y.shape[0])
        x_pad = np.concatenate([self.x, np.repeat(0, int(max_length-self.x.shape[0]))]) * gain_factor
        y_pad = np.concatenate([self.y, np.repeat(0, int(max_length-self.y.shape[0]))]) * gain_factor

        return x_pad, y_pad

fs_x, x = read_audio_file('./audio/large-hall.wav')
fs_y, y = read_audio_file('./audio/singing-female.wav')
c = Convolve(x, y).convolve_freq_complex()

write_audio_file(c, fs_x, './audio/processed-convolution-3.wav')
