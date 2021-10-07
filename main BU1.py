# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from functools import partial
import os
import time
import sys
import unittest
import inquirer
import librosa
import soundfile
import numpy as np
import noisereduce as nr
from scipy.io import wavfile

from colorama import Fore, Back, Style

from tempfile import (
    NamedTemporaryFile,
    mkdtemp,
    gettempdir
)
import tempfile
import struct

import simpleaudio as sa
from playsound import playsound
import pygame

from pydub import (
    AudioSegment,
    silence,
    effects,
    scipy_effects
)

from pydub.playback import play

from pydub.audio_segment import extract_wav_headers
from pydub.utils import (
    db_to_float,
    ratio_to_db,
    make_chunks,
    mediainfo,
    get_encoder_name,
    get_supported_decoders,
    get_supported_encoders,
)

import PySimpleGUI as sg

sg.theme('Default1')

# --- Creating the different pages in the program

layout1 = [
    [sg.Text('Welcome To Audiobook Engine', size=(30, 1), justification='center', font=("Helvetica", 25),
             relief=sg.RELIEF_RIDGE)],
    [sg.Text('Choose a file to be processed', justification='center')],
    [sg.InputText(key='-file1-'), sg.FileBrowse()],
    [sg.Button('Load File')]]

layout2 = [
    [sg.Text('Choose Processes', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Checkbox('Compression', default=True, key="-Comp-")],
    [sg.Button('Next', key='N1')]]

layout3 = [
    [sg.Text('Layout 3', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Checkbox('Compression', default=True, key="-Comp1-")],
    [sg.Button('Next', key='N2')]]

# --- Creating the wrapper layout

layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), sg.Column(layout3, visible=False, key='-COL3-')],
          [sg.Button('Exit')]]

# Create the Window
window = sg.Window('Audiobook Engine', layout)
# Event Loop to process "events"

layout = 1  # The currently visible layout

while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        quit()

    if event == 'Load File':
        print('Button Pressed')
        filename = values['-file1-']
        print("Loading: ", filename)
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=True)

    if event == 'N1':
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=True)

    if event == 'N2':
        window[f'-COL3-'].update(visible=False)
        window[f'-COL1-'].update(visible=True)

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    # if event == 'Cycle Layout':
    #     window[f'-COL{layout}-'].update(visible=False)
    #     layout = layout + 1 if layout < 3 else 1
    #     window[f'-COL{layout}-'].update(visible=True)
    # elif event in '123':
    #     window[f'-COL{layout}-'].update(visible=False)
    #     layout = int(event)
    #     window[f'-COL{layout}-'].update(visible=True)

window.close()

# ---Print Introduction Text
print(Fore.MAGENTA + " ")
print("   ▄████████ ███    █▄  ████████▄   ▄█   ▄██████▄  ▀█████████▄   ▄██████▄   ▄██████▄     ▄█   ▄█▄")
print("  ███    ███ ███    ███ ███   ▀███ ███  ███    ███   ███    ███ ███    ███ ███    ███   ███ ▄███▀")
print("  ███    ███ ███    ███ ███    ███ ███▌ ███    ███   ███    ███ ███    ███ ███    ███   ███▐██▀")
print("  ███    ███ ███    ███ ███    ███ ███▌ ███    ███  ▄███▄▄▄██▀  ███    ███ ███    ███  ▄█████▀   ")
print("▀███████████ ███    ███ ███    ███ ███▌ ███    ███ ▀▀███▀▀▀██▄  ███    ███ ███    ███ ▀▀█████▄")
print("  ███    ███ ███    ███ ███    ███ ███  ███    ███   ███    ██▄ ███    ███ ███    ███   ███▐██▄")
print("  ███    ███ ███    ███ ███   ▄███ ███  ███    ███   ███    ███ ███    ███ ███    ███   ███ ▀███▄")
print("  ███    █▀  ████████▀  ████████▀  █▀    ▀██████▀  ▄█████████▀   ▀██████▀   ▀██████▀    ███   ▀█▀")
print("                                                                                        ▀")
print("             ▄████████ ███▄▄▄▄      ▄██████▄   ▄█  ███▄▄▄▄      ▄████████")
print("            ███    ███ ███▀▀▀██▄   ███    ███ ███  ███▀▀▀██▄   ███    ███")
print("            ███    █▀  ███   ███   ███    █▀  ███▌ ███   ███   ███    █▀")
print("           ▄███▄▄▄     ███   ███  ▄███        ███▌ ███   ███  ▄███▄▄▄")
print("          ▀▀███▀▀▀     ███   ███ ▀▀███ ████▄  ███▌ ███   ███ ▀▀███▀▀▀")
print("            ███    █▄  ███   ███   ███    ███ ███  ███   ███   ███    █▄")
print("            ███    ███ ███   ███   ███    ███ ███  ███   ███   ███    ███")
print("            ██████████  ▀█   █▀    ████████▀  █▀    ▀█   █▀    ██████████  ")
print(" ")
print(Style.RESET_ALL)

print("Loading File...")
# file = input("--")

# ---Import Audio File
ABook = AudioSegment.from_file(filename, frame_rate=44100, channels=1, sample_width=2)
print("File Loaded")

while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        quit()
    if event == 'Next':
        if values["-Comp-"] == True:
            print("True")
        else:
            print("False")
        break
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

window.close()

# ---Generate checklist of processes to be run on the audio
questions = [
    inquirer.Checkbox('jobs',
                      message="Processes",
                      choices=[('Compression', 'Comp'),
                               ('Normalisation', 'Norm'),
                               ('Background Noise Reduction', 'NR'),
                               ('Mouth Noise Reduction', 'MNR'),
                               ('Vocal EQ', 'EQ'),
                               ('Silence Skipping', 'SilSkip'),
                               ('Adjust Speed', 'Speed'),
                               ('Librosa Test', 'libTest')
                               ],
                      ),
]

answers = inquirer.prompt(questions)
jobs = answers.get("jobs")
print(jobs)

if "libTest" in jobs:
    print("Librosa Test...")

    # samples = ABook.get_array_of_samples()
    #
    # fp_arr = np.array(samples).T.astype(np.float32)
    # fp_arr /= np.iinfo(samples[0].typecode).max
    #
    # y = librosa.effects.pitch_shift(fp_arr, n_steps=-1, sr=44100)
    # # --- Exports file again
    # soundfile.write("data/temp.wav", data=y, samplerate=44100)

if "Comp" in jobs:
    print("Compressing...")
    ABook = effects.compress_dynamic_range(ABook, threshold=-20.0, ratio=6.0, attack=5.0, release=50.0)

if "Norm" in jobs:
    print("Normalising...")
    ABook = effects.normalize(ABook, headroom=0.1)

if "NR" in jobs:
    print("Preparing Noise Reduction...")

    # ---Creating a sample of the background hiss

    # ---Detecting periods of silence over 700ms, then creating a list
    silenceList = dict(silence.detect_silence(ABook, min_silence_len=700, silence_thresh=-22, seek_step=1))
    keyList = [key for key in silenceList]
    print(silenceList)

    # ---Extracting the start and end points of the first period of silence
    FStart = (keyList[0])
    FEnd = silenceList[FStart]

    # ---Removing the beginning and end to ensure that the sample is clean
    FStart = FStart + 150
    FEnd = FEnd - 150

    print("FStart: ", FStart)
    print("FEnd: ", FEnd)

    # ---Saving it as it's own clip
    BGNoise = ABook[FStart:FEnd]
    BGNoise.export("data/BG.wav", format="wav")
    ABook.export("data/temp.wav", format="wav")

    y, sr = librosa.load("data/temp.wav", sr=44100, mono=True, res_type='linear')
    yNoise, sr = librosa.load("data/BG.wav", sr=44100, mono=True, res_type='linear')

    # perform noise reduction
    print("Reducing Noise...")
    reduced_noise = nr.reduce_noise(y=y, sr=sr, y_noise=yNoise, prop_decrease=0.5)

    soundfile.write("data/temp.wav", data=reduced_noise, samplerate=44100)

    # ---Loads new, shifted file up as ABook
    ABook = AudioSegment.from_file("data/temp.wav", format="wav", frame_rate=44100, channels=1, sample_width=2)

if "MNR" in jobs:
    print("Reducing Mouth Noises...")
    ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak", gain_dB=-30,
                             order=2)

if "EQ" in jobs:
    print("Equalizing...")
    ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak", gain_dB=-30,
                             order=2)

if 'SilSkip' in jobs:
    # ---Split file into non-silent sections
    print("Skipping Silence...")
    Short = silence.split_on_silence(ABook, min_silence_len=1200, silence_thresh=-30, seek_step=1, keep_silence=500)
    print("Segments Split")

    # --- Determine how many audio segments the silence skipper generated
    partnu = len(Short)
    print(partnu)

    # ---Create Blank Segment
    Output = AudioSegment.empty()
    len(Output) == 0

    # --Add each audio segment onto the end of the blank segment
    i = 0
    while i < partnu:
        clip = Short[i]
        Output = Output.append(clip, crossfade=0)
        # print([i])
        # print(clip)
        i = i + 1

    ABook = Output

if "Speed" in jobs:
    print("Adjusting Speed...")

    # --- Changes the frame rate of ABook to adjust speed (changes pitch too)
    ABook = ABook._spawn(ABook.raw_data, overrides={'frame_rate': 48510})

    # ---Export file so it can be loaded into librosa
    ABook.export("data/temp.wav", format="wav")

    # ---Load file into Librosa so it can be pitch shifted (Currently sounds bad)
    y, sr = librosa.load("data/temp.wav", sr=44100, mono=True, res_type='linear')
    y = ABook.get_array_of_samples()
    y = librosa.effects.pitch_shift(y, n_steps=-1, sr=44100)
    # --- Exports file again
    soundfile.write("data/temp.wav", data=y, samplerate=44100)

    # ---Loads new, shifted file up as ABook
    ABook = AudioSegment.from_file("data/temp.wav", format="wav", frame_rate=44100, channels=1, sample_width=2)

print("Exporting...")
ABook.export("files/newtower.mp3", format="mp3")

print("Now Playing")
# play(ABook)
print("Done")
time.sleep(5)
