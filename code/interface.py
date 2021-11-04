from tkinter import Label, Button, Tk
from audio_context import AudioContext

ctx = AudioContext()

window = Tk()
window.title('Null Test Application')

label = Label(window, text='Import an audio file and apply processing', font=('Arial', 20))
label.grid(column=0, row=0)

import_btn = Button(window, text='Import audio', fg='green', command=ctx.import_click)
import_btn.grid(column=0, row=1)

play_null_button = Button(window, text='Play null', command=ctx.play_null)
play_null_button.grid(column=0, row=2)

play_processed_button = Button(window, text='Play processed', command=ctx.play_processed)
play_processed_button.grid(column=0, row=3)

play_original_btn = Button(window, text='Play original', command=ctx.play_original)
play_original_btn.grid(column=0, row=4)

# window size
window.geometry('800x600')

window.mainloop()