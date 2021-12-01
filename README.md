# Project
A python app for useful audio utilities separated by tabs.

- Null-Test module
- Convolution module

# Description

* Null Test
A null test interface for visualizing audio effects processing in a waveform.

The app allows you to import a file, add a chain of audio effects using the pedalboard package by Spotify, and visualize the wave forms and frequency spectrum of the original signal, the processed signal, as well as the difference between them (null test).

A null-test is a useful method to determine what exactly a given audio process does to a signal. It does this by substracting the original signal from the processed signal, or adding the phase-shifted (180 degrees) original signal to the processed one.

* Convolution
A useful tool for sound design, this module allows the user to select two audio files and create a cross synthesis of them by applying a convolution algorithm. The user can listen and visualize the original and convolved audio signals for comparisson.

# Setup
    - Extract files or clone repository
    - In the extracted directory, setup virtual environment $ python3 -m venv ./
    - Activate the venv with $ source bin/activate
    - Install packages $ pip install -r requirements.txt
    - Run `$ python3 code/interface.py`
    - Deactivate the environment when finished $ deactivate

# Screenshot

![Alt text](./screenshot.png?raw=true "Null Test Application")