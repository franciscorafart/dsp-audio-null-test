from tkinter import Label, Button, Tk
from audio_context import AudioContext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

ctx = AudioContext()
window = Tk()

def click():
    ctx.import_click()
    fig, ((x1, k1), (x2, k2), (x3, k3)) = plt.subplots(3, 2)

    # NOTE: To display samples in seconds
    tx = np.arange(ctx.signal.shape[0]) / float(ctx.sample_rate)
    t_processedx = np.arange(ctx.processed_signal.shape[0]) / float(ctx.sample_rate)

    fig.suptitle('Signals')

    x1.set_ylim([-1,1])
    x2.set_ylim([-1,1])
    x3.set_ylim([-1,1])

    x1.plot(tx, ctx.signal, label='original signal')
    x2.plot(t_processedx, ctx.processed_signal, color='g', label='processed signal')
    x3.plot(t_processedx, ctx.null_signal, color='r', label='null test')

    # TODO: Plot spectrums with logarithmic scale
    tk = np.arange(12000)
    # k1.set_xscale('log')
    k1.plot(tk, ctx.signal_spectrum[0:12000])
    # k2.xscale('log')
    k2.plot(tk, ctx.processed_spectrum[0:12000], color='g')
    # k3.xscale('log')
    k3.plot(tk, ctx.null_spectrum[0:12000], color='r')

    canvas = FigureCanvasTkAgg(fig,
                               master = window)  
    canvas.draw()
  
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   window)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


window.title('Null Test Application')

label = Label(window, text='Import an audio file and apply processing', font=('Arial', 20))

import_btn = Button(window, text='Import audio', command=click)
import_btn.pack()

play_original_btn = Button(window, text='Play original', fg='blue', command=ctx.play_original)
play_original_btn.pack()

play_processed_button = Button(window, text='Play processed', fg='green', command=ctx.play_processed)
play_processed_button.pack()

play_null_button = Button(window, text='Play null', fg='red', command=ctx.play_null)
play_null_button.pack()

# window size
window.geometry('800x600')

window.mainloop()