from tkinter import Tk, ttk, Frame
from nulltest.nulltest_ui import NullTestUI
from convolution.convolution_ui import ConvolutionUI

class Interface():
    def __init__(self):
        self.window = Tk()
        tabControl = ttk.Notebook(self.window)

        tab1 = Frame(tabControl)
        tab2 = Frame(tabControl)

        tabControl.add(tab1, text ='Null Test')
        tabControl.add(tab2, text ='Convolution')
        tabControl.pack(expand = 1, fill ="both")

        self.tab2 = ConvolutionUI(tab2)
        self.tab1 = NullTestUI(tab1)

        self.window.title('Rafart Audio Utils')
        self.window.geometry('1200x900') # window size

    def mainloop(self):
        self.window.mainloop()

interface = Interface()
interface.mainloop()