# Project
Audio Null Test interface for signal processing

# Description
A null test interface for visualizing effects of audio processing in a waveform.

The app allows you to import a file, add a chain of audio effects using the pedalboard package by Spotify, and visualize the wave forms and frequency spectrum of the original signal, the processed signal, as well as the difference between them (null test).

# Technology
pedalboard api by spotify

# Setup
    - Extract files or clone repository
    - In the extracted directory, setup virtual environment $ python3 -m venv ./
    - Activate the venv with $ source bin/activate
    - Install packages $ pip install -r requirements.txt
    - Run `$ python3 code/interface.py`
    - Deactivate the environment when finished $ deactivate
