from tkinter import Label, Button, StringVar, Tk, OptionMenu, Entry, DoubleVar
from audio_context import AudioContext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from effects import Pedal, effect_map

class Interface():
    def __init__(self):
        self.window = Tk()
        self.pedal = Pedal()
        self.ctx = AudioContext()

        self.window.title('Null Test Application')
        self.window.geometry('1200x900') # window size

        self.import_btn = Button(self.window, text='Import Audio', command=self.import_file, width=8)
        self.import_btn.grid(row=0, column=0)

        self.process_btn = Button(self.window, text='Process Audio', command=self.process_audio_and_plot, state='disabled', width=8)
        self.process_btn.grid(row=0, column=1)
        self.filename = None

        self.dropdown = None
        self.menu = None

        # Buttons
        self.add_effect_btn = None
        self.play_original_btn = None
        self.play_processed_button = None
        self.play_null_button = None

        self.next_row_idx = 3

        self.figure = None
        # Effects storage
        self.effects = [] # {effect_key: xxx, config_params: [(param_key, Label, Entry)]}


    def mainloop(self):
        self.window.mainloop()

    def import_file(self):
        self.reset_ui_and_effects()
        self.filename = self.ctx.import_file()

        #Set the Menu initially
        menu = StringVar()
        menu.set('Select effect')

        self.menu = menu
        self.dropdown = OptionMenu(self.window, menu , *effect_map.keys())
        self.dropdown.grid(row=1, column=0)

        self.add_effect_btn = Button(self.window, text='+', command=self.add_effect, width=8)
        self.add_effect_btn.grid(row=1, column=1)

    def process_audio_and_plot(self):
        self.set_effect()

        self.remove_play_buttons()
        self.add_play_buttons()

        self.ctx.process(self.pedal)
        fig, ((x1, k1), (x2, k2), (x3, k3)) = plt.subplots(3, 2)

        self.figure = fig

        tx = np.arange(self.ctx.signal.shape[0]) / float(self.ctx.sample_rate) # display samples in seconds
        t_processedx = np.arange(self.ctx.processed_signal.shape[0]) / float(self.ctx.sample_rate)

        self.figure.suptitle('Signals for {}'.format(self.filename.split('/')[-1]))

        x1.set_ylim([-1,1])
        x2.set_ylim([-1,1])
        x3.set_ylim([-1,1])

        x1.plot(tx, self.ctx.signal, label='original signal')
        x2.plot(t_processedx, self.ctx.processed_signal, color='g', label='processed signal')
        x3.plot(t_processedx, self.ctx.null_signal, color='r', label='null test')

        tk = np.arange(12000)
        # k1.set_xscale('log')
        k1.plot(tk, self.ctx.signal_spectrum[0:12000])
        # k2.xscale('log')
        k2.plot(tk, self.ctx.processed_spectrum[0:12000], color='g')
        # k3.xscale('log')
        k3.plot(tk, self.ctx.null_spectrum[0:12000], color='r')

        # NOTE: Add pyplot to tkinter reference: https://www.geeksforgeeks.org/how-to-embed-matplotlib-charts-in-tkinter-gui/
        canvas = FigureCanvasTkAgg(fig, master = self.window)
        self.canvas = canvas
        self.canvas.draw()

        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().place(relx=0.5, rely=1, anchor='s')

        # creating the Matplotlib toolbar
        # toolbar = NavigationToolbar2Tk(self.canvas, self.window)  # TODO: Breaking here!
        # toolbar.update()
        # placing the toolbar on the Tkinter window
        # canvas.get_tk_widget().pack()

    def add_effect(self): # config
        effect_identifier = self.menu.get()

        effect_dict = effect_map[effect_identifier]
        effect_class = effect_dict['instance']
        default_config = effect_dict['config']

        effect_label = Label(self.window, text=effect_identifier.capitalize(), font=16)
        effect_label.grid(row=self.next_row_idx, column=1)

        config_params = []
        for param_key, v in default_config.items():
            param_index = len(config_params)
            default_value = DoubleVar()
            default_value.set(v)

            label = Label(self.window, text=param_key)
            param_entry = Entry(self.window, textvariable=default_value, width=5)

            label.grid(row=self.next_row_idx, column=(param_index*2)+2)
            param_entry.grid(row=self.next_row_idx, column= 1 + (param_index * 2) + 2)

            config_params.append((param_key, label, param_entry))

        self.next_row_idx = self.next_row_idx + 1

        self.effects.append({
            'effect': effect_class,
            'effect_label': effect_label,
            'config_params': config_params,
        })

        # Enable process button when first effect added only
        if len(self.effects) >= 1:
            self.process_btn.config(state="active")

    def set_effect(self):
        for effect in self.effects:
            effect_config = {}
            for (param_key, _, param_entry) in effect['config_params']:
                value = param_entry.get().replace('-', '').replace('.', '')
                if value.isdigit():
                    effect_config[param_key] = float(param_entry.get()) # TODO: Fix string issues for filter. Use is_number function to decide which type
                else:
                    mode = self.pedal.get_mode(param_entry.get())
                    if mode:
                        effect_config[param_key] = mode


            self.pedal.add_effect(effect['effect'], effect_config)


    def add_play_buttons(self):
        self.play_original_btn = Button(self.window, text='Play original', fg='blue', command=self.ctx.play_original)
        self.play_original_btn.grid(row=self.next_row_idx, column=0)

        self.play_processed_button = Button(self.window, text='Play processed', fg='green', command=self.ctx.play_processed)
        self.play_processed_button.grid(row=self.next_row_idx, column=1)

        self.play_null_button = Button(self.window, text='Play null', fg='red', command=self.ctx.play_null)
        self.play_null_button.grid(row=self.next_row_idx, column=2)

        self.next_row_idx = self.next_row_idx + 1

    def reset_ui_and_effects(self):
        if self.process_btn:
            self.process_btn.config(state='disabled')

        self.remove_play_buttons()

        # Remove effects UI
        for effect in self.effects:
            effect['effect_label'].destroy()

            for (_, label, entry) in effect['config_params']:
                label.destroy()
                entry.destroy()

        self.effects = []
        if self.dropdown:
            self.dropdown.destroy()
            self.dropdown = None
            self.menu = None

        if self.add_effect_btn:
            self.add_effect_btn.destroy()

        self.pedal.clear_effects()

    def remove_play_buttons(self):
        if self.play_original_btn:
            self.play_original_btn.destroy()
        if self.play_processed_button:
            self.play_processed_button.destroy()
        if self.play_null_button:
            self.play_null_button.destroy()

interface = Interface()
interface.mainloop()