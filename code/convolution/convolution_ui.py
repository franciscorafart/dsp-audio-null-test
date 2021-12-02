from tkinter import Button, StringVar, Tk, ttk, Frame
from convolution.convolution import Convolve
from audio_utils import play_audio_file, import_file, spectrum
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np
from audio_utils import write_audio_file

class ConvolutionUI():
    def __init__(self, tab):
        self.tab = tab

        self.import_btn1 = Button(self.tab, text='Import Audio 1', command=lambda: self.import_file(1), width=8)
        self.import_btn1.grid(row=0, column=0)

        self.import_btn2 = Button(self.tab, text='Import Audio 2', command=lambda: self.import_file(2), width=8)
        self.import_btn2.grid(row=0, column=1)
        self.convolved = None

        self.filename1 = None
        self.filename2 = None
        self.convolve_file = './audio/processed-convolution-3.wav'

    def import_file(self, i):
        if (i==1):
            self.filename1 = import_file()
        elif(i==2):
            self.filename2 = import_file()

        self.allow_process()

    def allow_process(self):
        if (self.filename1 and self.filename2):
            self.add_effect_btn = Button(self.tab, text='Convolve', command=self.convolve, width=8)
            self.add_effect_btn.grid(row=1, column=1)

    def convolve(self):
        self.convolved = Convolve(self.filename1, self.filename2)
        x = self.convolved.convolve_freq_complex()

        write_audio_file(x, self.convolved.fs, self.convolve_file)
        self.add_play_buttons()
        self.process_audio_and_plot()

    def add_play_buttons(self):
        self.play_original_btn = Button(self.tab, text='Play audio 1', fg='blue', command=lambda: play_audio_file(self.filename1))
        self.play_original_btn.grid(row=2, column=0)

        self.play_processed_button = Button(self.tab, text='Play audio 2', fg='green', command=lambda: play_audio_file(self.filename2))
        self.play_processed_button.grid(row=2, column=1)

        self.play_null_button = Button(self.tab, text='Play convolution', fg='red', command=lambda: play_audio_file(self.convolve_file))
        self.play_null_button.grid(row=2, column=2)

    # TODO: 1. Add wave visualization / 2. Add Entry to determine export file name

    def process_audio_and_plot(self):
        fig, ((x1, k1), (x2, k2), (x3, k3)) = plt.subplots(3, 2)

        self.figure = fig

        tx = np.arange(self.convolved.x.shape[0]) / float(self.convolved.fs) # display samples in seconds
        ty = np.arange(self.convolved.y.shape[0]) / float(self.convolved.fs) # display samples in seconds
        tz = np.arange(self.convolved.z.shape[0]) / float(self.convolved.fs) # display samples in seconds

        # t_processedx = np.arange(self.ctx.processed_signal.shape[0]) / float(self.ctx.sample_rate)
        self.figure.suptitle('Convolution {} and {}'.format(self.filename1.split('/')[-1], self.filename2.split('/')[-1]))

        x1.set_ylim([-1,1])
        x2.set_ylim([-1,1])
        x3.set_ylim([-1,1])

        x1.plot(tx, self.convolved.x, label='Audio 1')
        x2.plot(ty, self.convolved.y, color='g', label='Audio 2')
        x3.plot(tz, self.convolved.z, color='r', label='Convolved audio')

        # tk = np.arange(12000)
        xk, yk, zk = self.convolved.get_real_spectrums()

        k1.plot(xk[0:12000])
        k2.plot(yk[0:12000], color='g')
        k3.plot(zk[0:12000], color='r')

        # NOTE: Add pyplot to tkinter reference: https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/
        canvas = FigureCanvasTkAgg(fig, master = self.tab)
        self.canvas = canvas
        self.canvas.draw()

        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().place(relx=0.5, rely=1, anchor='s')
