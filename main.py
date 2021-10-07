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

sg.theme('Default1')

# --- Creating the different pages in the program

# --- Home screen
LOHome = [
    # [sg.Text("   ▄████████ ███    █▄  ████████▄   ▄█   ▄██████▄  ▀█████████▄   ▄██████▄   ▄██████▄     ▄█   ▄█▄")],
    # [sg.Text("  ███    ███ ███    ███ ███   ▀███ ███  ███    ███   ███    ███ ███    ███ ███    ███   ███ ▄███▀")],
    # [sg.Text("  ███    ███ ███    ███ ███    ███ ███▌ ███    ███   ███    ███ ███    ███ ███    ███   ███▐██▀")],
    # [sg.Text("  ███    ███ ███    ███ ███    ███ ███▌ ███    ███  ▄███▄▄▄██▀  ███    ███ ███    ███  ▄█████▀   ")],
    # [sg.Text("▀███████████ ███    ███ ███    ███ ███▌ ███    ███ ▀▀███▀▀▀██▄  ███    ███ ███    ███ ▀▀█████▄")],
    # [sg.Text("  ███    ███ ███    ███ ███    ███ ███  ███    ███   ███    ██▄ ███    ███ ███    ███   ███▐██▄")],
    # [sg.Text("  ███    ███ ███    ███ ███   ▄███ ███  ███    ███   ███    ███ ███    ███ ███    ███   ███ ▀███▄")],
    # [sg.Text("  ███    █▀  ████████▀  ████████▀  █▀    ▀██████▀  ▄█████████▀   ▀██████▀   ▀██████▀    ███   ▀█▀")],
    # [sg.Text("                                                                                        ▀")],
    # [sg.Text("             ▄████████ ███▄▄▄▄      ▄██████▄   ▄█  ███▄▄▄▄      ▄████████")],
    # [sg.Text("            ███    ███ ███▀▀▀██▄   ███    ███ ███  ███▀▀▀██▄   ███    ███")],
    # [sg.Text("            ███    █▀  ███   ███   ███    █▀  ███▌ ███   ███   ███    █▀")],
    # [sg.Text("           ▄███▄▄▄     ███   ███  ▄███        ███▌ ███   ███  ▄███▄▄▄")],
    # [sg.Text("          ▀▀███▀▀▀     ███   ███ ▀▀███ ████▄  ███▌ ███   ███ ▀▀███▀▀▀")],
    # [sg.Text("            ███    █▄  ███   ███   ███    ███ ███  ███   ███   ███    █▄")],
    # [sg.Text("            ███    ███ ███   ███   ███    ███ ███  ███   ███   ███    ███")],
    # [sg.Text("            ██████████  ▀█   █▀    ████████▀  █▀    ▀█   █▀    ██████████  ")],
    [sg.Text('Welcome To Audiobook Engine', size=(30, 1), justification='center', font=("Helvetica", 25),
             relief=sg.RELIEF_RIDGE)],
    [sg.Text('Choose a file to be processed', justification='center')],
    [sg.InputText(key='-file1-', default_text='C:/Users/Richard/Documents/GitHub/Audiobooks/files/tower.wav'),
     sg.FileBrowse()],
    [sg.Button('Load File', key='NHome')]]

# ---Select Processes Screen
LOProcess = [
    [sg.Text('Choose Processes', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Checkbox('Compression', default=False, key="-Comp-")],
    [sg.Checkbox('Normalisation', default=False, key="-Norm-")],
    [sg.Checkbox('Background Noise Reduction', default=False, key="-NR-")],
    [sg.Checkbox('Mouth Noise Reduction', default=False, key="-MNR-")],
    [sg.Checkbox('Vocal EQ', default=False, key="-EQ-")],
    [sg.Checkbox('Silence Skipping', default=False, key="-SSkip-")],
    [sg.Checkbox('Adjust Speed', default=False, key="-Speed-")],
    [sg.Checkbox('Librosa Test', default=False, key="-libtest-")],
    [sg.Button('Next', key='NProcesses')]]

# --- Compression Screen
LOComp = [
    [sg.Text('Compression', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Button('Next', key='NComp')]]

# --- Normalisation Screen
LONorm = [
    [sg.Text('Normalisation', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Button('Next', key='NNorm')]]

# --- Background Noise Reduction Screen
LONR = [
    [sg.Text('Background Noise Reduction', size=(30, 1), justification='center', font=("Helvetica", 25),
             relief=sg.RELIEF_RIDGE)],
    [sg.Button('Next', key='NNR')]]

# --- Mouth Noise Reduction Screen
LOMNR = [
    [sg.Text('Mouth Noise Reduction', size=(30, 1), justification='center', font=("Helvetica", 25),
             relief=sg.RELIEF_RIDGE)],
    [sg.Button('Next', key='NMNR')]]

# --- Vocal EQ Screen
LOEQ = [
    [sg.Text('Vocal EQ', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.InputCombo(('Default', 'Boost Lows', 'Boost Highs', 'Weird'), default_value='Default', size=(20, 1),
                   key='EQcombo',
                   enable_events=True)],
    [sg.Frame('Manual EQ', [
        [sg.Frame('32', [
            [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq32', enable_events=True)],
            #[sg.InputText('0', size=(3, 1), key='ieq32', enable_events=True)]
        ]),
         sg.Frame('64', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq64', enable_events=True)],
             #[sg.InputText(size=(3, 1), key='ieq64', enable_events=True)]
         ]),
         sg.Frame('125', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq125', enable_events=True)],
             #[sg.InputText(size=(3, 1), key='ieq125', enable_events=True)]
         ]),
         sg.Frame('250', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq250', enable_events=True)],
             #[sg.InputText(size=(3, 1), key='ieq250', enable_events=True)]
         ]),
         sg.Frame('500', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq500', enable_events=True)],
             #[sg.InputText(size=(3, 1), key='ieq500', enable_events=True)]
         ]),
         sg.Frame('1k', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq1k', enable_events=True)],
             #[sg.InputText(size=(3, 1), key='ieq1k', enable_events=True)]
         ]),
         sg.Frame('2k', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq2k', enable_events=True)],
             #[sg.InputText(size=(3, 1), key='ieq2k', enable_events=True)]
         ]),
         sg.Frame('4k', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq4k', enable_events=True)],
             #[sg.InputText(size=(3, 1), key='ieq4k', enable_events=True)]
         ]),
         sg.Frame('8k', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq8k', enable_events=True)],
             #[sg.InputText(size=(3, 1), key='ieq8k', enable_events=True)]
         ]),
         sg.Frame('16k', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq16k', enable_events=True)],
             #[sg.InputText(size=(3, 1), key='ieq16k', enable_events=True,)]
         ])],
    ])],
    [sg.Button('Next', key='NEQ')]]

# --- Silence Skipping Screen
LOSSkip = [
    [sg.Text('Silence Skipping', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Button('Next', key='NSSkip')]]

# --- Adjust Speed Screen
LOSpeed = [
    [sg.Text('Adjust Speed', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Button('Next', key='NSpeed')]]

# --- Librosa Test Screen
LOlibtest = [
    [sg.Text('Librosa Test', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Button('Next', key='Nlibtest')]]

# --- Export Screen
LOExport = [
    [sg.Text('Export', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.Button('Next', key='NExport')]]

# --- Creating the wrapper layout
layout = [[sg.Column(LOHome, key='-LOHome'),
           sg.Column(LOProcess, visible=False, key='-LOProcess'),
           sg.Column(LOComp, visible=False, key='-LOComp'),
           sg.Column(LONorm, visible=False, key='-LONorm'),
           sg.Column(LONR, visible=False, key='-LONR'),
           sg.Column(LOMNR, visible=False, key='-LOMNR'),
           sg.Column(LOEQ, visible=False, key='-LOEQ'),
           sg.Column(LOSSkip, visible=False, key='-LOSSkip'),
           sg.Column(LOSpeed, visible=False, key='-LOSpeed'),
           sg.Column(LOlibtest, visible=False, key='-LOlibtest'),
           sg.Column(LOExport, visible=False, key='-LOExport')
           ],
          [sg.Button('Exit')]]

# ---Creating and populating the list of pages (To be added to on the processes page)
Pages = ['-LOHome', '-LOProcess']
Page = 0

# ---Defining Vocal EQ Settings
EQPSDefault = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EQPSWeird = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
# Create the Window
window = sg.Window('Audiobook Engine', layout)

# Event Loop to process "events"
while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        quit()

# ---Events for Home Screen
    if event == 'NHome':
        print("Loading File...")
        filename = values['-file1-']
        print("Loading: ", filename)

        # ---Import Audio File
        ABook = AudioSegment.from_file(filename, frame_rate=44100, channels=1, sample_width=2)
        print("File Loaded")

        window[Pages[Page]].update(visible=False)
        Page = Page + 1
        window[Pages[Page]].update(visible=True)

# ---Events for Processes Screen
    if event == 'NProcesses':
        # --- Compression
        if values['-Comp-'] == True:
            Comp = True
            Pages.append('-LOComp')
        else:
            Comp = False

        # --- Normalisation
        if values['-Norm-'] == True:
            Norm = True
            Pages.append('-LONorm')
        else:
            Norm = False

        # --- Background Noise Reduction
        if values['-NR-'] == True:
            NR = True
            Pages.append('-LONR')
        else:
            NR = False

        # --- Mouth Noise Reduction
        if values['-MNR-'] == True:
            MNR = True
            Pages.append('-LOMNR')
        else:
            MNR = False

        # --- Vocal EQ
        if values['-EQ-'] == True:
            EQ = True
            Pages.append('-LOEQ')
        else:
            EQ = False

        # --- Silence Skipping
        if values['-SSkip-'] == True:
            SSkip = True
            Pages.append('-LOSSkip')
        else:
            SSkip = False

        # --- Adjust Speed
        if values['-Speed-'] == True:
            Speed = True
            Pages.append('-LOSpeed')
        else:
            Speed = False

        # --- Librosa Test
        if values['-libtest-'] == True:
            libtest = True
            Pages.append('-LOlibtest')
        else:
            libtest = False

        Pages.append('-LOExport')

        print(Pages)

        window[Pages[Page]].update(visible=False)
        Page = Page + 1
        window[Pages[Page]].update(visible=True)

# ---Events for Compression Screen
    if event == 'NComp':
        print("Compressing...")
        ABook = effects.compress_dynamic_range(ABook, threshold=-20.0, ratio=6.0, attack=5.0, release=50.0)

        window[Pages[Page]].update(visible=False)
        Page = Page + 1
        window[Pages[Page]].update(visible=True)

# ---Events for Normalisation Screen
    if event == 'NNorm':
        print("Normalising...")
        ABook = effects.normalize(ABook, headroom=0.1)

        window[Pages[Page]].update(visible=False)
        Page = Page + 1
        window[Pages[Page]].update(visible=True)

# ---Events for Background Noise Reduction Screen
    if event == 'NNR':
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

        window[Pages[Page]].update(visible=False)
        Page = Page + 1
        window[Pages[Page]].update(visible=True)

# ---Events for Mouth Noise Reduction Screen
    if event == 'NMNR':
        print("Reducing Mouth Noises...")
        ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak",
                                 gain_dB=-30,
                                 order=2)

        window[Pages[Page]].update(visible=False)
        Page = Page + 1
        window[Pages[Page]].update(visible=True)

# ---Events for Vocal EQ Screen

    # ---EQ Sliders
    if event == 'eq32' or 'eq64' or 'eq125' or 'eq250' or 'eq500' or 'eq1k' or 'eq2k' or 'eq4k' or 'eq8k' or 'eq16k':
        window['EQcombo'].update('Custom')

    # ---Combo Box
    if event == 'EQcombo':
        if values['EQcombo'] == 'Default':
            eqname = 'Default'
            eqsetting = EQPSDefault

        if values['EQcombo'] == 'Weird':
            eqname = 'Weird'
            eqsetting = EQPSWeird

        window['eq32'].update(eqsetting[0])
        window['eq64'].update(eqsetting[1])
        window['eq125'].update(eqsetting[2])
        window['eq250'].update(eqsetting[3])
        window['eq500'].update(eqsetting[4])
        window['eq1k'].update(eqsetting[5])
        window['eq2k'].update(eqsetting[6])
        window['eq4k'].update(eqsetting[7])
        window['eq8k'].update(eqsetting[8])
        window['eq16k'].update(eqsetting[9])

        print(eqname)
        window['EQcombo'].update(eqname)

    # --- Input Boxes
    # if event == 'ieq32':
    #     if values['ieq32'] == '2':
    #         eqvalue = 0
    #     else:
    #         eqvalue = int(values['ieq32'])
    #         if eqvalue < -15:
    #             eqvalue = -15
    #         if eqvalue > 15:
    #             eqvalue = 15
    #     window['eq32'].update(eqvalue)
    #     window['ieq32'].update(eqvalue)

    # ---Next Button
    if event == 'NEQ':
        print("Equalizing...")

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak",
                                 gain_dB=-30, order=2)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak",
                                 gain_dB=-30, order=2)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak",
                                 gain_dB=-30, order=2)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak",
                                 gain_dB=-30, order=2)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak",
                                 gain_dB=-30, order=2)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak",
                                 gain_dB=-30, order=2)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak",
                                 gain_dB=-30, order=2)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak",
                                 gain_dB=-30, order=2)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak",
                                 gain_dB=-30, order=2)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak",
                                 gain_dB=-30, order=2)

        window[Pages[Page]].update(visible=False)
        Page = Page + 1
        window[Pages[Page]].update(visible=True)

# ---Events for Silence Skipping Screen
    if event == 'NSSkip':
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

        window[Pages[Page]].update(visible=False)
        Page = Page + 1
        window[Pages[Page]].update(visible=True)

# ---Events for Adjust Speed Screen
    if event == 'NSpeed':
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

        window[Pages[Page]].update(visible=False)
        Page = Page + 1
        window[Pages[Page]].update(visible=True)

# ---Events for Librosa Test Screen
    if event == 'Nlibtest':
        print("Librosa Test...")

        # samples = ABook.get_array_of_samples()
        #
        # fp_arr = np.array(samples).T.astype(np.float32)
        # fp_arr /= np.iinfo(samples[0].typecode).max
        #
        # y = librosa.effects.pitch_shift(fp_arr, n_steps=-1, sr=44100)
        # # --- Exports file again
        # soundfile.write("data/temp.wav", data=y, samplerate=44100)

        window[Pages[Page]].update(visible=False)
        Page = Page + 1
        window[Pages[Page]].update(visible=True)

# ---Events for Export Screen
    if event == 'NExport':
        print("Exporting...")
        ABook.export("files/newtower.mp3", format="mp3")

        print("Now Playing")
        # play(ABook)
        print("Done")

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

window.close()
