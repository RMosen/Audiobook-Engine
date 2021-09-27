# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from functools import partial
import os
import time
import sys
import unittest
import inquirer
import scipy

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


# ---Print Introduction Text
print("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
print("█░▄▄▀██░██░██░▄▄▀█▄░▄██░▄▄▄░██░▄▄▀██░▄▄▄░██░▄▄▄░██░█▀▄████░▄▄▄██░▀██░██░▄▄░█▄░▄██░▀██░██░▄▄▄")
print("█░▀▀░██░██░██░██░██░███░███░██░▄▄▀██░███░██░███░██░▄▀█████░▄▄▄██░█░█░██░█▀▀██░███░█░█░██░▄▄▄")
print("█░██░██▄▀▀▄██░▀▀░█▀░▀██░▀▀▀░██░▀▀░██░▀▀▀░██░▀▀▀░██░██░████░▀▀▀██░██▄░██░▀▀▄█▀░▀██░██▄░██░▀▀▀")
print("▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀")

print("Loading File...")
# file = input("--")

# ---Import Audio File
ABook = AudioSegment.from_file("files/it.wav", format="wav", frame_rate=44100, channels=2, sample_width=2)
print("File Loaded")



# ---Generate checklist of processes to be run on the audio
questions = [
  inquirer.Checkbox('jobs',
                    message="Processes",
                    choices=[('Normalisation', 'Norm'),
                             ('Vocal EQ', 'EQ'),
                             ('Silence Skipping', 'SilSkip'),
                             ('Compression', 'Comp')
                             ],
                    ),
]

answers = inquirer.prompt(questions)
jobs = answers.get("jobs")
print(jobs)

if "Norm" in jobs:
    print("Normalising...")
    ABook = effects.normalize(ABook, headroom=5)

if "EQ" in jobs:
    print("Equalizing...")
    ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=100, channel_mode="L+R", filter_mode="peak", gain_dB=-30, order=2)

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
        #print([i])
        #print(clip)
        i = i + 1

    ABook = Output

if "Comp" in jobs:
    print("Compressing")
    ABook = effects.compress_dynamic_range(ABook, threshold=-20.0, ratio=6.0, attack=5.0, release=50.0)

print("Exporting...")
ABook.export("files/newit.wav", format="wav")



#print("Now Playing")
#pygame.mixer.init()
#pygame.mixer.music.load("files/newit.mp3")
#pygame.mixer.music.play()
print("Done")
time.sleep(3)