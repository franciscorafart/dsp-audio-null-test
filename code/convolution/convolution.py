import numpy as np
from audio_utils import spectrum, complex_spectrum, read_audio_file
import scipy.fftpack as fftpack

class Convolve():
    def __init__(self, file1, file2):
        fs_x, x = read_audio_file(file1)
        fs_y, y = read_audio_file(file2)

        if (fs_x != fs_y):
            raise Exception('Files must have same sample rate')

        self.x = x
        self.y = y
        self.z = None


        self.fs = fs_x


    def set_real_spectrum(self, gain_factor=0.1):
        x_pad, y_pad = self._zero_pad(gain_factor)
        self.spectrum_y = spectrum(y_pad)
        self.spectrum_x = spectrum(x_pad)

    def set_complex_spectrum(self, gain_factor=0.1):
        x_pad, y_pad = self._zero_pad(gain_factor)
        self.complex_spectrum_y = complex_spectrum(y_pad)
        self.complex_spectrum_x = complex_spectrum(x_pad)

    # NOTE: Doing convolution by doing fft -> multiplying the frequency domains -> doing inverse fft. O(n log(n))
    def convolve_freq_complex(self):
        self.set_complex_spectrum()

        self.complex_spectrum_z = self.complex_spectrum_y * self.complex_spectrum_x
        self.complex_z = fftpack.ifft(self.complex_spectrum_z)

        self.z = np.real(self.complex_z)

        return self.complex_z

    # NOTE: Doing convolution by doing fft -> multiplying the frequency domains -> doing inverse fft. O(n log(n))
    # Doing it only in the real spectrum (cuts the audio duration)
    def convolve_freq_real(self):
        self.set_real_spectrum()
        convolution = self.spectrum_y * self.spectrum_x
        self.z = fftpack.irfft(convolution)

        return self.z

    def get_real_spectrums(self):
        if self.z is None:
            return spectrum(self.x), spectrum(self.y), np.array([])

        return spectrum(self.x), spectrum(self.y), spectrum(self.z)



    # NOTE: Direct convolution in the time domain - O(N^2)
    def convolve_time_domain(self, gain_factor=0.1):
        max_length = max(self.x.shape[0], self.y.shape[0])
        x_pad = np.concatenate([self.x, np.repeat(0, int(max_length-self.x.shape[0]))]) * gain_factor
        y_pad = np.concatenate([self.y, np.repeat(0, int(max_length-self.y.shape[0]))]) * gain_factor
        self.z = np.convolve(x_pad, y_pad)
        return self.z

    # Jeff Wang's implementation of convolution algorithm O(N^2)
    def convolve(x, y):
        z = [0] * (len(x) + len(y) - 1)
        for i, v in enumerate(x):
            for j, w in enumerate(y):
                z[i+j] += v*w
        return z

        # Test case
        # Plan      *  Patient List   = Total Daily Usage

        # [3 2 1]   *  [1 2 3 4 5]    = [3 8 14 20 26 14 5]
        #               M T W T F        M T W  T  F  S  S

    def _zero_pad(self, gain_factor=0.1):
        max_length = self.x.shape[0] + self.y.shape[0] - 1
        # max_length = max(self.x.shape[0], self.y.shape[0])
        x_pad = np.concatenate([self.x, np.repeat(0, int(max_length-self.x.shape[0]))]) * gain_factor
        y_pad = np.concatenate([self.y, np.repeat(0, int(max_length-self.y.shape[0]))]) * gain_factor

        return x_pad, y_pad

