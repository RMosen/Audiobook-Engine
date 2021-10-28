import os.path
import sys
import time
import re
import numpy as np
import array
import noisereduce as nr
import simpleaudio as sa
from pydub import (
    AudioSegment,
    silence,
    effects,
    scipy_effects,
    playback)
import PySimpleGUI as sg

# You've just crossed over into...

#    ▄████████ ███    █▄  ████████▄   ▄█   ▄██████▄  ▀█████████▄   ▄██████▄   ▄██████▄     ▄█   ▄█▄
#   ███    ███ ███    ███ ███   ▀███ ███  ███    ███   ███    ███ ███    ███ ███    ███   ███ ▄███▀
#   ███    ███ ███    ███ ███    ███ ███▌ ███    ███   ███    ███ ███    ███ ███    ███   ███▐██▀
#   ███    ███ ███    ███ ███    ███ ███▌ ███    ███  ▄███▄▄▄██▀  ███    ███ ███    ███  ▄█████▀
# ▀███████████ ███    ███ ███    ███ ███▌ ███    ███ ▀▀███▀▀▀██▄  ███    ███ ███    ███ ▀▀█████▄
#   ███    ███ ███    ███ ███    ███ ███  ███    ███   ███    ██▄ ███    ███ ███    ███   ███▐██▄
#   ███    ███ ███    ███ ███   ▄███ ███  ███    ███   ███    ███ ███    ███ ███    ███   ███ ▀███▄
#   ███    █▀  ████████▀  ████████▀  █▀    ▀██████▀  ▄█████████▀   ▀██████▀   ▀██████▀    ███   ▀█▀
#                                                                                         ▀
#              ▄████████ ███▄▄▄▄      ▄██████▄   ▄█  ███▄▄▄▄      ▄████████
#             ███    ███ ███▀▀▀██▄   ███    ███ ███  ███▀▀▀██▄   ███    ███
#             ███    █▀  ███   ███   ███    █▀  ███▌ ███   ███   ███    █▀
#            ▄███▄▄▄     ███   ███  ▄███        ███▌ ███   ███  ▄███▄▄▄
#           ▀▀███▀▀▀     ███   ███ ▀▀███ ████▄  ███▌ ███   ███ ▀▀███▀▀▀
#             ███    █▄  ███   ███   ███    ███ ███  ███   ███   ███    █▄
#             ███    ███ ███   ███   ███    ███ ███  ███   ███   ███    ███
#             ██████████  ▀█   █▀    ████████▀  █▀    ▀█   █▀    ██████████

# ---Presets

# ---Noise Reduction Presets
# ---[Noise Reduction Amount]
NRPS0 = 0
NRPS25 = 25
NRPS50 = 50
NRPS75 = 75

NRPSNames = ['0', '25', '50', '75']
NRPSValues = [NRPS0, NRPS25, NRPS50, NRPS75]

# ---Compression Presets
# ---[Threshold, Ratio, Attack, Release]
CompPSDefault = [0, 0, 0, 0]
CompPSBasic = [-8.4, 16, 2, 800]

CompPSNames = ['Default', 'Basic']
CompPSValues = [CompPSDefault, CompPSBasic]

# ---Normalisation Presets
# ---[Target Volume]
NormPSDefault = 0
NormPSLouder = 2
NormPSMuchLouder = 4
NormPSQuieter = -3
NormPSMuchQuieter = -6

NormPSNames = ['Default', 'Louder', 'Much Louder', 'Quieter', 'Much Quieter']
NormPSValues = [NormPSDefault, NormPSLouder, NormPSMuchLouder, NormPSQuieter, NormPSMuchQuieter]

# ---Vocal EQ Presets
# ---[32Hz, 64Hz, 125Hz, 250Hz, 500Hz, 1kHz, 2kHz, 4kHz, 8kHz, 16kHz]
EQPSDefault = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EQPSBoomyVoice = [-9, -7, -5, -3, 1, 2, 2, 2, 3, 3]

EQPSNames = ['Default', 'Boomy Voice']
EQPSValues = [EQPSDefault, EQPSBoomyVoice]

# ---Silence Skipping Presets
# ---[Minimum Silence, Silence Threshold, Keep Silence, Searching Step]
SSPSDefault = [1200, -30, 600, 2]
SSPSNoSilenceDetected = [1200, -40, 600, 2]
SSPSSkippingTooMuch = [1200, -20, 600, 2]
SSPSLongerSilence = [2400, -30, 900, 2]
SSPSShorterSilence = [900, -30, 300, 2]

SSkipPSNames = ['Default', 'No Silence Detected', 'Skipping Too Much', 'Longer Silence', 'Shorter Silence']
SSkipPSValues = [SSPSDefault, SSPSNoSilenceDetected, SSPSSkippingTooMuch, SSPSLongerSilence, SSPSShorterSilence]

# ---Creating the theme
sg.LOOK_AND_FEEL_TABLE['ABETheme'] = {'BACKGROUND': '#180D2B',
                                      'TEXT': '#FFF3CC',
                                      'INPUT': '#FFFFFF',
                                      'TEXT_INPUT': '#000000',
                                      'SCROLL': '#2F1042',
                                      'BUTTON': ('#000000', '#F3CC49'),
                                      'PROGRESS': ('#D1826B', '#CC8019'),
                                      'BORDER': 1, 'SLIDER_DEPTH': 0,
                                      'PROGRESS_DEPTH': 0, }
sg.theme('ABETheme')

# --- Setting the fonts

# ---Header Fonts
Header = ("Century Schoolbook Bold", 25)
HeaderC = '#F3CC49'
HeaderBG = '#2F1042'

# --- Main Fonts
Font = ('Helvetica', 11)

# --- Info Button Fonts
infoc = '#F77959'

# --- Creating the different pages in the program
# --- Home screen
LOHome = [
    [sg.Image('files/logo.png')],
    [sg.Text('Choose a file to be processed', justification='center', font=Font)],
    [sg.InputText(key='applyHome',
                  default_text='',
                  disabled=True, enable_events=True, font=Font),
     sg.FilesBrowse(file_types=(("Audio Files", "*.wav *.mp3 *.flac"), ("All Files", "*")), key='HomeFB'),
     ]
]

# ---Select Processes Screen
LOProcess = [
    [sg.Text('Choose Processes', justification='center', font=Header, text_color=HeaderC)],
    [sg.Frame('', [
        [sg.Text('🛈', key='infoPrNR', enable_events=True, text_color=infoc),
         sg.Checkbox('Background Noise Reduction', default=False, key="-NR-")],
        [sg.Text('🛈', key='infoPrComp', enable_events=True, text_color=infoc),
         sg.Checkbox('Compression', default=False, key="-Comp-")],
        [sg.Text('🛈', key='infoPrNorm', enable_events=True, text_color=infoc),
         sg.Checkbox('Normalisation', default=False, key="-Norm-")],
        [sg.Text('🛈', key='infoPrEQ', enable_events=True, text_color=infoc),
         sg.Checkbox('Vocal EQ', default=False, key="-EQ-")],
        [sg.Text('🛈', key='infoPrSSkip', enable_events=True, text_color=infoc),
         sg.Checkbox('Silence Skipping', default=False, key="-SSkip-")],
    ], element_justification='Left', relief=sg.RELIEF_FLAT)]
]

# --- Background Noise Reduction Screen
LONR = [
    [sg.Text('Background Noise Reduction', justification='center', font=Header, text_color=HeaderC),
     sg.Text('🛈', key='infoNR', font=Header, enable_events=True, text_color=infoc)],
    [sg.InputCombo(NRPSNames, default_value='50%', size=(4, 1),
                   key='NRCombo',
                   enable_events=True)],
    [sg.Frame('Noise Reduction Amount', [
        [sg.InputText(key="VNR", size=(4, 1), default_text='50', pad=(0, 30)), sg.Text('%')]
    ], element_justification='c')],

    [sg.Button('Apply', key='applyNR', enable_events=True),
     sg.Button('⟲', key='undoNR', enable_events=True, disabled=True)]
]

# --- Compression Screen
LOComp = [
    [sg.Text('Compression', justification='center', font=Header, text_color=HeaderC),
     sg.Text('🛈', key='infoComp', font=Header, enable_events=True, text_color=infoc)],
    [sg.InputCombo(CompPSNames, default_value='Default', size=(20, 1),
                   key='CompCombo',
                   enable_events=True)],
    [sg.Frame('Manual Compressor', [
        [sg.Text('🛈', key='infoCompThresh', enable_events=True, text_color=infoc),
         sg.Text('Threshold:', size=(8, 1)),
         sg.InputText(key="CompThreshold", size=(4, 1), default_text='0', enable_events=True),
         sg.Text('dB', size=(3, 1))],

        [sg.Text('🛈', key='infoCompRatio', enable_events=True, text_color=infoc),
         sg.Text('Ratio:', size=(8, 1)),
         sg.InputText(key="CompRatio", size=(4, 1), default_text='1', enable_events=True), sg.Text(':1', size=(3, 1))],

        [sg.Text('🛈', key='infoCompAttack', enable_events=True, text_color=infoc),
         sg.Text('Attack:', size=(8, 1)),
         sg.InputText(key="CompAttack", size=(4, 1), default_text='3', enable_events=True), sg.Text('ms', size=(3, 1))],

        [sg.Text('🛈', key='infoCompRelease', enable_events=True, text_color=infoc),
         sg.Text('Release:', size=(8, 1)),
         sg.InputText(key="CompRelease", size=(4, 1), default_text='100', enable_events=True),
         sg.Text('ms', size=(3, 1))],

        [sg.Button('Apply', key='applyComp', enable_events=True),
         sg.Button('⟲', key='undoComp', enable_events=True, disabled=True)]

    ], element_justification='c')],
]

# --- Normalisation Screen
LONorm = [
    [sg.Text('Normalisation', justification='center', font=Header, text_color=HeaderC),
     sg.Text('🛈', key='infoNorm', font=Header, enable_events=True, text_color=infoc)],
    [sg.InputCombo(NormPSNames, default_value='Default', size=(20, 1),
                   key='NormCombo',
                   enable_events=True)],
    [sg.Frame('Normalisation Target', [
        # [sg.Text('Headroom:', size=(8, 1)), sg.InputText(key="VNorm", size=(4, 1), default_text='0')]
        [sg.Slider(range=(-20, 5), default_value=0, orientation='h', key='VNorm',
                   enable_events=True, pad=20, resolution=0.5, )]
    ])],

    [sg.Button('Apply', key='applyNorm', enable_events=True),
     sg.Button('⟲', key='undoNorm', enable_events=True, disabled=True)]
]


# --- Vocal EQ Screen
LOEQ = [
    [sg.Frame('', [
        [sg.Text('Vocal EQ', justification='center', font=Header, text_color=HeaderC),
         sg.Text('🛈', key='infoEQ', font=Header, enable_events=True, text_color=infoc)],
    ], size=(700, 1), border_width=0)],
    [sg.InputCombo(EQPSNames, default_value='Default', size=(20, 1),
                   key='EQCombo',
                   enable_events=True)],
    [sg.Frame('', [
        [sg.Frame('32', [
            [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq32', enable_events=True)],
            # [sg.InputText('0', size=(3, 1), key='ieq32', enable_events=True)]
        ]),
         sg.Frame('64', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq64', enable_events=True)],
             # [sg.InputText(size=(3, 1), key='ieq64', enable_events=True)]
         ]),
         sg.Frame('125', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq125', enable_events=True)],
             # [sg.InputText(size=(3, 1), key='ieq125', enable_events=True)]
         ]),
         sg.Frame('250', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq250', enable_events=True)],
             # [sg.InputText(size=(3, 1), key='ieq250', enable_events=True)]
         ]),
         sg.Frame('500', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq500', enable_events=True)],
             # [sg.InputText(size=(3, 1), key='ieq500', enable_events=True)]
         ]),
         sg.Frame('1k', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq1k', enable_events=True)],
             # [sg.InputText(size=(3, 1), key='ieq1k', enable_events=True)]
         ]),
         sg.Frame('2k', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq2k', enable_events=True)],
             # [sg.InputText(size=(3, 1), key='ieq2k', enable_events=True)]
         ]),
         sg.Frame('4k', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq4k', enable_events=True)],
             # [sg.InputText(size=(3, 1), key='ieq4k', enable_events=True)]
         ]),
         sg.Frame('8k', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq8k', enable_events=True)],
             # [sg.InputText(size=(3, 1), key='ieq8k', enable_events=True)]
         ]),
         sg.Frame('16k', [
             [sg.Slider(range=(-15, 15), default_value=0, orientation='vertical', key='eq16k', enable_events=True)],
             # [sg.InputText(size=(3, 1), key='ieq16k', enable_events=True,)]
         ])],
        [sg.Button('Apply', key='applyEQ', enable_events=True),
         sg.Button('⟲', key='undoEQ', enable_events=True, disabled=True)]
    ], element_justification='c', border_width=0)],
]

# --- Silence Skipping Screen
LOSSkip = [
    [sg.Text('Silence Skipping', justification='center', font=Header, text_color=HeaderC),
     sg.Text('🛈', key='infoSSkip', font=Header, enable_events=True, text_color=infoc)],
    [sg.InputCombo(SSkipPSNames, default_value='Default', size=(20, 1),
                   key='SSkipCombo',
                   enable_events=True)],

    [sg.Frame('Silence Skipping', [
        [sg.Text('🛈', key='infoSSkipMin', enable_events=True, text_color=infoc),
         sg.Text('Minimum Silence:', size=(14, 1)), sg.InputText(key="SSMin", size=(5, 1), default_text='1200'),
         sg.Text('ms', size=(3, 1))],

        [sg.Text('🛈', key='infoSSkipThresh', enable_events=True, text_color=infoc),
         sg.Text('Silence Threshold:', size=(14, 1)), sg.InputText(key="SSThresh", size=(5, 1), default_text='-30'),
         sg.Text('dB', size=(3, 1))],

        [sg.Text('🛈', key='infoSSkipKeep', enable_events=True, text_color=infoc),
         sg.Text('Keep Silence:', size=(14, 1)), sg.InputText(key="SSKeep", size=(5, 1), default_text='500'),
         sg.Text('ms', size=(3, 1))],

        [sg.Text('🛈', key='infoSSkipStep', enable_events=True, text_color=infoc),
         sg.Text('Searching Step:', size=(14, 1)), sg.InputText(key="SSStep", size=(5, 1), default_text='1'),
         sg.Text('ms', size=(3, 1))],

        [sg.Button('Apply', key='applySS', enable_events=True),
         sg.Button('⟲', key='undoSS', enable_events=True, disabled=True)]
    ])]
]

# --- Defining ExportFormat
ExportFormat = ('mp3', '.mp3')
# --- Export Screen
LOExport = [
    [sg.Text('Export', justification='center', font=Header, text_color=HeaderC),
     sg.Text('🛈', key='infoExport', font=Header, enable_events=True, text_color=infoc)],

    [sg.Text('Export Folder', justification='center')],
    [sg.InputText(key='-file2-', default_text=''),
     sg.FileSaveAs(file_types=(('Wav', '*.wav'), ('MP3', '*.mp3'), ('Flac', '*.flac')), key='ExportSA')],
    [sg.Button('Export', key='applyExport')],
    [sg.Button('Restart', key='Restart', visible=False)]
]


# --- Info Box
LOInfo = [
    [sg.Text('Info')],
    [sg.Frame('', [
        [sg.Text(" ", key='info', size=(15, 19),
                 background_color=HeaderBG, font=('Helvetica', 9))]
    ], background_color=HeaderBG)]
]


# --- Audio Player1 (For Screens without audio editing capabilities)
LOPlay1 = [
    [sg.Frame('', [[sg.Text('Play/Stop', background_color=HeaderBG),
                    sg.Button('▶', key='play', disabled=True, size=(4, 2)),
                    sg.Button('⯀', key='stop', disabled=True, size=(4, 2))]
                   ], background_color=HeaderBG, border_width=0, element_justification='c', font=('Courier New', 300),
              pad=(0, 20))]
]

# --- Audio Player2 (For Screens with audio editing capabilities)
LOPlay2 = [
    [sg.Frame('', [[sg.Frame('', [[sg.Text('Original', background_color=HeaderBG, size=(6, 1)),
                                   sg.Button('▶', key='play2', disabled=True, size=(2, 1))],

                                  [sg.Text('Modified', background_color=HeaderBG, size=(6, 1)),
                                   sg.Button('▶', key='play3', disabled=True, size=(2, 1))]
                                  ], border_width=0, background_color=HeaderBG),
                    sg.Frame('', [[sg.Button('⯀', key='stop2', disabled=True, size=(4, 2))]
                                  ], border_width=0, background_color=HeaderBG)]
                   ], background_color=HeaderBG, border_width=0)
     ]
]

# --- Next and Skip buttons
LONext = [
    [sg.Button('Skip', key='-skip-', enable_events=True, disabled=False, size=(8, 2), visible=False)],
    [sg.Button('Next', key='-next-', enable_events=True, disabled=True, size=(8, 2))]
]

# --- A spacer to help get the layout right
LOSpacer = [
    [sg.Text('', size=(20, 1))]
]

# --- Creating the main layout
layout = [
    [sg.Frame('', [
        [sg.Frame('', [
            # --- The Main window. Includes everything apart from the player, the next/skip button, and the info box
            [sg.TabGroup([
                [sg.Tab('Home', LOHome, visible=False, disabled=True, key='-LOHome', element_justification='c'),
                 sg.Tab('Processes', LOProcess, visible=False, disabled=True, key='-LOProcess',
                        element_justification='c'),
                 sg.Tab('NR', LONR, visible=False, disabled=True, key='-LONR', element_justification='c'),
                 sg.Tab('Comp', LOComp, visible=False, disabled=True, key='-LOComp', element_justification='c'),
                 sg.Tab('Norm', LONorm, visible=False, disabled=True, key='-LONorm', element_justification='c'),
                 sg.Tab('EQ', LOEQ, visible=False, disabled=True, key='-LOEQ', element_justification='c'),
                 sg.Tab('SSkip', LOSSkip, visible=False, disabled=True, key='-LOSSkip', element_justification='c'),
                 sg.Tab('Export', LOExport, visible=False, disabled=True, key='-LOExport', element_justification='c'),
                 ]],
                selected_background_color='#180D2B',
                size=(700, 350),
                expand_x=True,
                expand_y=True,
                border_width=2,
                tab_location='topleft',
                key='MainFrame',
            )],

            # ---The two notification bars that appear just above Next/Skip
            [sg.Text('', key='ExportBar', justification='c', visible=False)],
            [sg.Text('', key='NBar', justification='c', visible=True)],

            # ---The Audio Player
            [sg.TabGroup([
                [sg.Tab('Player', LOPlay1, visible=True, disabled=False, key='-LOPlay1', element_justification='c',
                        background_color=HeaderBG),
                 sg.Tab('Player', LOPlay2, visible=False, disabled=True, key='-LOPlay2', element_justification='c',
                        background_color=HeaderBG)
                 ]],
                tab_location='topleft',
                selected_background_color=HeaderBG,
                border_width=2,
                pad=4
            ),

                # --- The Next/Skip buttons and the spacer
                sg.Column(LONext, visible=True, key='-LONext', element_justification='c', pad=(110, 0)),
                sg.Column(LOSpacer, visible=True, key='-LOSpacer', element_justification='c', pad=(5, 0)),
            ]
        ], element_justification='c', border_width=0),

        # --- The Info Box
         sg.Column(LOInfo, visible=False, key='-LOInfo', element_justification='c')]
    ], background_color='#180D2B', border_width=10, relief=sg.RELIEF_FLAT, pad=20, element_justification='c')]
]

# ---Creating and populating the list of pages (To be added to on the processes page)
Pages = ['-LOHome', '-LOProcess']
Page = 0

# Create the Window
window = sg.Window('Audiobook Engine',
                   layout,
                   no_titlebar=False,
                   use_custom_titlebar=True,
                   grab_anywhere=False,
                   titlebar_background_color='#2F1042',
                   titlebar_text_color='#ffffff',
                   titlebar_font=('Helvetica', 11),
                   margins=(12, 12),
                   element_padding=5,
                   element_justification='Center',
                   font=('Arial Nova', 11),
                   background_color='#F77959',
                   titlebar_icon='',
                   resizable=False,
                   )

# --- Defining a couple things
skip = False
count = 0

# Event Loop to process events in the program
while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        sys.exit()

    # print(event)

    # ---Events for the play button
    if event in ['play', 'play3']:
        print('Play')
        sa.stop_all()
        window['stop'].update(disabled=False)
        window['stop2'].update(disabled=False)
        window.refresh()
        playback._play_with_simpleaudio(ABook)

    # ---Events for play original button
    if event == 'play2':
        print('Play2')
        sa.stop_all()
        window['stop'].update(disabled=False)
        window['stop2'].update(disabled=False)
        window.refresh()
        playback._play_with_simpleaudio(Prev)

    # ---Events for stop button
    if event in ['stop', 'stop2']:
        window['stop'].update(disabled=True)
        window['stop2'].update(disabled=True)
        window.refresh()
        print('Stop')
        sa.stop_all()

    # --- What happens when you press undo
    if event in ['undoComp', 'undoNorm', 'undoNR', 'undoMNR', 'undoEQ', 'undoSS']:
        ABook = Prev
        window['undoComp'].update(disabled=True)
        window['undoNorm'].update(disabled=True)
        window['undoNR'].update(disabled=True)
        window['undoMNR'].update(disabled=True)
        window['undoEQ'].update(disabled=True)
        window['undoSS'].update(disabled=True)
        window['play3'].update(disabled=True)
        window['-next-'].update(disabled=True)

    # ---What happens when you click Skip
    if event == "-skip-":
        answer = sg.popup_yes_no(
            'Skip this process?', no_titlebar=True, background_color=infoc, font=('Helvetica', 11), text_color='black')

        if answer == 'No':
            print('No')
        else:
            print('Yes')
            ABook = Prev
            skip = True
            event = '-next-'

    # ---What happens when you click next
    if event == '-next-':

        # ---The edited audiobook becomes the backup state when you press next
        Prev = ABook

        sa.stop_all()
        window['NBar'].update('')
        window['play3'].update(disabled=True)
        window['undoComp'].update(disabled=True)
        window['undoNorm'].update(disabled=True)
        window['undoNR'].update(disabled=True)
        window['undoMNR'].update(disabled=True)
        window['undoEQ'].update(disabled=True)
        window['undoSS'].update(disabled=True)
        window['play3'].update(disabled=True)
        window['-LOInfo'].update(visible=True)
        window['-next-'].update(disabled=True)
        window['ExportBar'].update(visible=False)

        window['info'].update("Click on one of the 🛈's to see more information.")

        # --- Events for Processes page
        # --- Checks to see if a box is ticked, and adds it to the list of pages if so
        if Pages[Page] == "-LOProcess":
            # --- Background Noise Reduction
            if values['-NR-'] == True:
                NR = True
                Pages.append('-LONR')
            else:
                NR = False

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

            Pages.append('-LOExport')

            print(Pages)

        # --- Progress main page to next screen
        Page = Page + 1
        window[Pages[Page]].select()
        window[Pages[(Page - 1)]].update(visible=False, disabled=True)

        # --- Removing a page from the export task list if the page is skipped
        if skip == True:
            Pages.remove(Pages[Page - 1])
            Page = Page - 1
        skip = False

        print(Pages[Page])
        # --- Choose player and skip button based on which screen is open
        if Pages[Page] in ["-LOHome", "-LOProcess", "-LOExport"]:
            window['-LOPlay1'].select()
            window['-LOPlay2'].update(visible=False, disabled=True)
            window['-skip-'].update(visible=False)
        else:
            window['-LOPlay2'].select()
            window['-LOPlay1'].update(visible=False, disabled=True)
            window['-skip-'].update(visible=True)

        # --- Disables/Hides the next button for certain pages
        if Pages[Page] == "-LOProcess":
            window['-next-'].update(disabled=False)

        if Pages[Page] == "-LOExport":
            window['-next-'].update(visible=False)

        window.refresh()

    # --- What happens when you click apply
    if event in ['applyHome', 'applyComp', 'applyNorm', 'applyNR', 'applyMNR', 'applyEQ', 'applySS', 'applyExport']:
        sa.stop_all()
        window['play'].update(disabled=True)
        window['play2'].update(disabled=True)
        window['play3'].update(disabled=True)
        window['stop'].update(disabled=True)
        window['stop2'].update(disabled=True)
        window['-next-'].update(disabled=True)
        window['undoComp'].update(disabled=True)
        window['undoNorm'].update(disabled=True)
        window['undoNR'].update(disabled=True)
        window['undoMNR'].update(disabled=True)
        window['undoEQ'].update(disabled=True)
        window['undoSS'].update(disabled=True)
        window.refresh()

        # --Home Page (What happens when you click the browse button)
        if Pages[Page] == '-LOHome':
            print("Loading File...")
            window['NBar'].update('Loading File...')
            window.refresh()

            # --- Getting list of selected files
            filename = values['applyHome']

            # --- Converting into a python readable list
            filelist = re.split(r"\s*[,;]\s*", filename.strip())
            filecount = len(filelist)
            print(filelist)
            print(filecount)

            # --- Making sure the field isn't blank
            if filelist[0] == '':
                print("No File Selected")
                window['NBar'].update('No File Selected')
                window.refresh()
            else:
                print("Loading: ", filelist[0])

                # ---Import Audio File
                # --- Initially, only 60 seconds of the file is loaded, that makes messing around with settings faster
                # --- Files are imported in mono. Audiobooks don't need to be in stereo
                ABook = AudioSegment.from_file(filelist[0], channels=1, sample_width=2, frame_rate=44100, duration=60)
                # --- Creating Prev, the "Undo" state of the process
                Prev = ABook
                print("File Loaded")
                window['NBar'].update('File Loaded')
                window.refresh()
                window['-next-'].update(disabled=False)

        # --- Resetting the active file to the backup whenever a new effect is applied
        if Pages[Page] != '-LOHome':
            ABook = Prev

        # --- This area will loop if the program is exporting multiple files
        exporting = 1
        while exporting == 1:

            # --Exporting Part 1
            print('Pages:', Pages)
            if Pages[Page] == '-LOExport':
                if exporting == 0:
                    count = 0
                    exporting = 1

                # --- Loading the full audiobook for processing
                ABook = AudioSegment.from_file(filelist[count], channels=1, sample_width=2, frame_rate=44100)
                # ---Showing a second notification bar that shows "Processing 1 of 2" while the file is exporting
                window['ExportBar'].update(visible=True)
                progress = str('Processing file ' + str(count + 1) + ' of ' + str(filecount))
                print(progress)
                window['ExportBar'].update(progress)
                window['NBar'].update('Preparing to Export...')
                window.refresh()
                # --- A short sleep so that people see "Preparing to Export..." for a half second before it changes
                time.sleep(0.5)

            # --Noise Reduction
            if '-LONR' in Pages and Pages[Page] in ['-LONR', '-LOExport']:
                print("Preparing Noise Reduction...")
                window['NBar'].update('Preparing Background Noise Reduction...')
                window.refresh()

                # ---Reading input values
                NoiseReduction = int(values['VNR'])
                NoiseReduction = (NoiseReduction * 0.01)

                # ---Creating a sample of the background hiss
                # ---Detecting periods of silence over 700ms, then creating a list
                silenceList = dict(silence.detect_silence(ABook, min_silence_len=700, silence_thresh=-22, seek_step=3))
                keyList = [key for key in silenceList]
                # print(silenceList)

                # ---Extracting the start and end points of the first period of silence
                FStart = (keyList[0])
                FEnd = silenceList[FStart]

                # ---Removing the beginning and end to ensure that the sample is clean
                FStart = FStart + 150
                FEnd = FEnd - 150

                # print("FStart: ", FStart)
                # print("FEnd: ", FEnd)

                # ---Saving the silence it as it's own clip, then converting it to a NumPy array
                BGNoise = ABook[FStart:FEnd]
                bgsamples = BGNoise.get_array_of_samples()
                yNoise = np.array(bgsamples)

                # ---Converting ABook into a NumPy array
                samples = ABook.get_array_of_samples()
                y = np.array(samples)

                # perform noise reduction
                print("Reducing Noise...")
                window['NBar'].update('Reducing Background Noise...')
                window.refresh()
                reduced_noise = nr.reduce_noise(y=y, sr=44100, y_noise=yNoise, prop_decrease=NoiseReduction)

                # ---Converting file back to PyDub Segment
                shifted_samples_array = array.array(ABook.array_type, reduced_noise)
                ABook = ABook._spawn(shifted_samples_array)
                window['NBar'].update('Background Noise Reduced')
                window.refresh()

            # --Compression
            if '-LOComp' in Pages and Pages[Page] in ['-LOComp', '-LOExport']:
                print("Compressing...")
                window['NBar'].update('Compressing (this may take a while)...')
                window.refresh()

                # ---Reading input values
                threshold = int(values['CompThreshold'])
                ratio = int(values['CompRatio'])
                attack = int(values['CompAttack'])
                release = int(values['CompRelease'])

                # ---Applying compression
                ABook = effects.compress_dynamic_range(ABook, threshold=threshold, ratio=ratio, attack=attack,
                                                       release=release)

                window['NBar'].update('Compression Completed')
                window.refresh()

            # --Normalisation
            if '-LONorm' in Pages and Pages[Page] in ['-LONorm', '-LOExport']:
                print(values['VNorm'])

                # ---Reading input values
                normvalue = float(values['VNorm'])
                normvalue = (normvalue * -1)

                print("Normalising...")
                # print(normvalue)
                window['NBar'].update('Normalising...')
                window.refresh()

                # ---Applying normalisation
                ABook = effects.normalize(ABook, headroom=normvalue)
                window['NBar'].update('Normalisation Completed')
                window.refresh()

            # --Equaliser
            if '-LOEQ' in Pages and Pages[Page] in ['-LOEQ', '-LOExport']:
                print("Equalizing...")
                window['NBar'].update('Equalizing...')
                window.refresh()
                RO = 2
                ABook = ABook - 10

                # --- 32Hz
                print("32Hz")
                window['NBar'].update('Equalizing 0% Completed')
                window.refresh()
                # if values['eq32'] != 0:
                # --- Applying Eq (reading the input slider is done inline)
                ABook = scipy_effects.eq(ABook, focus_freq=32, bandwidth=21, filter_mode="peak",
                                         gain_dB=values['eq32'], order=RO)

                # --- 64Hz
                print("64Hz")
                window['NBar'].update('Equalizing 10% Completed')
                window.refresh()
                ABook = scipy_effects.eq(ABook, focus_freq=64, bandwidth=43, filter_mode="peak",
                                         gain_dB=values['eq64'], order=RO)

                # --- 125Hz
                print("125Hz")
                window['NBar'].update('Equalizing 20% Completed')
                window.refresh()
                ABook = scipy_effects.eq(ABook, focus_freq=125, bandwidth=79, filter_mode="peak",
                                         gain_dB=values['eq125'], order=RO)

                # --- 250Hz
                print("250Hz")
                window['NBar'].update('Equalizing 30% Completed')
                window.refresh()
                ABook = scipy_effects.eq(ABook, focus_freq=250, bandwidth=171, filter_mode="peak",
                                         gain_dB=values['eq250'], order=RO)

                # --- 500Hz
                print("500Hz")
                window['NBar'].update('Equalizing 40% Completed')
                window.refresh()
                ABook = scipy_effects.eq(ABook, focus_freq=500, bandwidth=329, filter_mode="peak",
                                         gain_dB=values['eq500'], order=RO)

                # --- 1kHz
                print("1kHz")
                window['NBar'].update('Equalizing 50% Completed')
                window.refresh()
                ABook = scipy_effects.eq(ABook, focus_freq=1000, bandwidth=671, filter_mode="peak",
                                         gain_dB=values['eq1k'], order=RO)

                # --- 2kHz
                print("2kHz")
                window['NBar'].update('Equalizing 60% Completed')
                window.refresh()
                ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=1329, filter_mode="peak",
                                         gain_dB=values['eq2k'], order=RO)

                # --- 4kHz
                print("4kHz")
                window['NBar'].update('Equalizing 70% Completed')
                window.refresh()
                ABook = scipy_effects.eq(ABook, focus_freq=4000, bandwidth=2671, filter_mode="peak",
                                         gain_dB=values['eq4k'], order=RO)

                # --- 8kHz
                print("8kHz")
                window['NBar'].update('Equalizing 80% Completed')
                window.refresh()
                ABook = scipy_effects.eq(ABook, focus_freq=8000, bandwidth=5329, filter_mode="peak",
                                         gain_dB=values['eq8k'], order=RO)

                # --- 16kHz
                print("16kHz")
                window['NBar'].update('Equalizing 90% Completed')
                window.refresh()
                ABook = scipy_effects.eq(ABook, focus_freq=16000, bandwidth=10671, filter_mode="peak",
                                         gain_dB=values['eq16k'], order=RO)

                ABook = ABook + 10
                window['NBar'].update('Equalization Complete')
                window.refresh()

            # --Silence Skipper
            if '-LOSSkip' in Pages and Pages[Page] in ['-LOSSkip', '-LOExport']:

                # ---Reading input values
                SSMin = int(values['SSMin'])
                SSThresh = int(values['SSThresh'])
                SSKeep = int(values['SSKeep'])
                SSStep = int(values['SSStep'])

                print("Skipping Silence...")
                window['NBar'].update('Skipping Silence...')
                window.refresh()

                # ---Split file into non-silent sections
                Short = silence.split_on_silence(ABook, min_silence_len=SSMin, silence_thresh=SSThresh, seek_step=SSStep,
                                                 keep_silence=SSKeep)
                print("Segments Split")

                # --- Determine how many audio segments the silence skipper generated
                partnu = len(Short)
                # print(Short)
                # print(partnu)

                # ---Making sure that there were segments generated (Otherwise there is no audio and things break)
                if partnu == 0:
                    print("No Silence Detected")
                    window['NBar'].update('No Silence Detected')
                    window.refresh()
                else:
                    # ---Create Blank Segment
                    Temp = AudioSegment.empty()
                    len(Temp) == 0

                    # --Append each audio segment onto the end of the blank segment
                    i = 0
                    while i < partnu:
                        Clip = Short[i]
                        Temp = Temp.append(Clip, crossfade=0)
                        # print([i])
                        # print(clip)
                        i = i + 1

                    ABook = Temp

                    window['NBar'].update('Silence Skipping Complete')
                    window.refresh()

            # --Export part 2
            if Pages[Page] == '-LOExport':
                # ---Generating a placeholder file. This is the best way I found of getting python to see what file-
                # ---extension was chosen by the user
                if count == 0:
                    export = values['-file2-']
                    placeholder = AudioSegment.empty()
                    placeholder.export(export)

                # ---Reading the placeholder file to see it's file extension
                formatfinder = os.path.splitext(export)
                FileExtension = str(formatfinder[1])
                print("File Extension: ", FileExtension)
                if FileExtension == '.mp3':
                    ExportFormat = 'mp3'

                if FileExtension == '.wav':
                    ExportFormat = 'wav'

                if FileExtension == '.flac':
                    ExportFormat = 'flac'

                # --- Adding a number onto the end of the file name if multiple files are being exported
                if count > 0:
                    countstr = str(count + 1)
                    extension = countstr + FileExtension
                    export = re.sub(FileExtension, extension, values['-file2-'])
                    print('out = ', export)

                print("Exporting...")
                window['NBar'].update('Exporting...')
                window.refresh()

                # ---Exporting the file
                ABook.export(export, bitrate='128k', format=ExportFormat)
                window.refresh()

                count = count + 1
                print(count)

                # ---Events for after exporting the last file
                if count == filecount:
                    exporting = 0
                    count = 0
                    window['NBar'].update('Exporting Complete')
                    print('Exporting Complete')
                    window['Restart'].update(visible=True)

            # --- Making the events not loop if the current page isn't export
            if Pages[Page] != '-LOExport':
                exporting = 0

        # --- Enabling the next button for after effects are applied
        if Pages[Page] != '-LOHome':
            window['-next-'].update(disabled=False)

        window['play'].update(disabled=False)
        window['play2'].update(disabled=False)
        window['play3'].update(disabled=False)
        window['undoComp'].update(disabled=False)
        window['undoNorm'].update(disabled=False)
        window['undoNR'].update(disabled=False)
        window['undoMNR'].update(disabled=False)
        window['undoEQ'].update(disabled=False)
        window['undoSS'].update(disabled=False)
        window.refresh()

    # ---Events for Restart Button (after file is exported)
    if event == 'Restart':
        Page = 0
        window[Pages[Page]].select()
        window['-LOExport'].update(visible=False, disabled=True)
        window['Restart'].update(visible=False)
        window['NBar'].update('')
        window['ExportBar'].update('', visible=False)
        window['-next-'].update(disabled=True, visible=True)
        window['applyHome'].update('')
        window['play'].update(disabled=True)
        Pages = ['-LOHome', '-LOProcess']
        window.refresh()

# ---Events for Background Noise Combo Box (Reading Presets)
    if event == 'NRCombo':
        print(values['NRCombo'])
        NRPSNum = NRPSNames.index(values['NRCombo'])
        print(NRPSNum)

        print(NRPSValues[NRPSNum])
        NRSetting = NRPSValues[NRPSNum]

        window['VNR'].update(NRSetting)


# ---Events for Compression Combo Box (Reading Presets)
    if event == 'CompCombo':
        print(values['CompCombo'])
        CompPSNum = CompPSNames.index(values['CompCombo'])
        print(CompPSNum)

        print(CompPSValues[CompPSNum])
        CompSetting = CompPSValues[CompPSNum]

        print('Comp Setting :', CompSetting)

        window['CompThreshold'].update(CompSetting[0])
        window['CompRatio'].update(CompSetting[1])
        window['CompAttack'].update(CompSetting[2])
        window['CompRelease'].update(CompSetting[3])


# ---Events for Normalisation Combo Box (Reading Presets)
    if event == 'NormCombo':
        print(values['NormCombo'])
        NormPSNum = NormPSNames.index(values['NormCombo'])
        print(NormPSNum)

        print(NormPSValues[NormPSNum])
        NormSetting = NormPSValues[NormPSNum]

        print('Norm Setting :', NormSetting)

        window['VNorm'].update(NormSetting)


# ---Events for Vocal EQ Combo Box (Reading Presets)
    if event == 'EQCombo':
        print(values['EQCombo'])
        EQPSNum = EQPSNames.index(values['EQCombo'])
        print(EQPSNum)

        print(EQPSValues[EQPSNum])
        EQSetting = EQPSValues[EQPSNum]

        print('eq setting :', EQSetting)

        window['eq32'].update(EQSetting[0])
        window['eq64'].update(EQSetting[1])
        window['eq125'].update(EQSetting[2])
        window['eq250'].update(EQSetting[3])
        window['eq500'].update(EQSetting[4])
        window['eq1k'].update(EQSetting[5])
        window['eq2k'].update(EQSetting[6])
        window['eq4k'].update(EQSetting[7])
        window['eq8k'].update(EQSetting[8])
        window['eq16k'].update(EQSetting[9])

# ---Events for Silence Skipping Combo Box (Reading Presets)
    if event == 'SSkipCombo':
        print(values['SSkipCombo'])
        SSkipPSNum = SSkipPSNames.index(values['SSkipCombo'])
        print(SSkipPSNum)

        print(SSkipPSValues[SSkipPSNum])
        SSkipSetting = SSkipPSValues[SSkipPSNum]

        print('SSkip setting :', SSkipSetting)

        window['SSMin'].update(SSkipSetting[0])
        window['SSThresh'].update(SSkipSetting[1])
        window['SSKeep'].update(SSkipSetting[2])
        window['SSStep'].update(SSkipSetting[3])


# ---The Info Buttons
    # ---Info Buttons for Presets Page
    if event == 'infoPrNR':
        window['info'].update('The Background Noise Reducer gets rid of any hiss, buzz,'
                              ' or other consistent background noise in your audiobook.')

    if event == 'infoPrComp':
        window['info'].update('The Compressor makes the loud parts of your audiobook quieter, giving the whole'
                              ' thing a more consistent volume')

    if event == 'infoPrNorm':
        window['info'].update('The Normaliser adjusts the volume of the whole audiobook,'
                              ' bringing it to a set level.\n\n'
                              'This is useful for making the audiobook the same volume as all your other audio files')

    if event == 'infoPrEQ':
        window['info'].update('The Equaliser Adjusts the volume of the different pitches,'
                              ' or frequencies, in the audiobook.\n\n'
                              'This is useful for reducing the bass, increasing the high end, or anything in between')

    if event == 'infoPrSSkip':
        window['info'].update('The Silence Skipper detects long pauses in the audiobook and removes them.')

    # ---Info Buttons for Noise Reduction Page
    if event == 'infoNR':
        window['info'].update('The Background Noise Reducer will detect background noise in the audiobook'
                              ' and attempt to reduce it.\n\n'
                              'This feature can make the rest of the audiobook sound weird if '
                              'it’s used too strongly, so play around and see what works for you'
                              ' (I recommend around 50%).')

    # ---Info Buttons for Compression Page
    if event == 'infoComp':
        window['info'].update('The Compressor makes it that the whole audiobook is of a similar volume.'
                              ' This makes for a more comfortable listening experience.\n\n'
                              'The compressor can be a bit confusing, so I’d recommend sticking to the presets'
                              ' unless you know what you’re doing.')

    if event == 'infoCompThresh':
        window['info'].update('The Threshold is the volume that audio has to go over'
                              ' to be effected by the compressor.\n\n'
                              "Set this lower if the compressor doesn't seem to be doing anything,"
                              " and higher if all it's doing is making the audio quieter (it will be quieter overall "
                              "anyway).")

    if event == 'infoCompRatio':
        window['info'].update('When part of the audiobook goes over the volume set by the Threshold, it will be reduced'
                              ' by the ratio specified in the ratio box.\n\n'
                              'Set this number higher to make the compressor more effective, but having it too high'
                              ' can sound weird, so use with caution.')

    if event == 'infoCompAttack':
        window['info'].update('The attack specifies how long it takes the compressor to lower the volume by the ratio'
                              ' specified by the ratio box after it goes over the'
                              ' volume specified in the threshold box.\n\n'
                              'Setting this number lower makes the volume more consistent, but it makes the volume'
                              ' changes very unnatural sounding.')

    if event == 'infoCompRelease':
        window['info'].update('The release specifies how long it takes the compressor to turn off after the volume'
                              ' of the audiobook goes below the threshold.\n\n'
                              'Having this number too low can make parts of the audiobook quieter that you would'
                              ' like, but too high can sound unnatural.')

    # ---Info Buttons for Normalisation Page
    if event == 'infoNorm':
        window['info'].update('The Normaliser adjusts the overall volume of the track.\n\n'
                              'I recommend leaving this'
                              ' one at zero, but feel free to play around and see what works for you.')

    # ---Info Buttons for Equaliser Page
    if event == 'infoEQ':
        window['info'].update('The Equaliser adjusts the volume of different frequencies/pitches of audio. '
                              'The higher numbers represent the higher frequencies and vice versa.\n\n'
                              'This is useful for if your audiobook sounds too bassy, too high pitched, or anywhere '
                              'in between.')

    # ---Info Buttons for Silence Skip Page
    if event == 'infoSSkip':
        window['info'].update('The Silence skipper detects periods of silence in the audiobook and shortens them.'
                              ' This can save you a lot of time in the long run, and can be un-noticeable'
                              ' with the right settings.')

    if event == 'infoSSkipMin':
        window['info'].update('The Minimum Silence is how long a period of silence'
                              ' has to be before it is shortened.\n\n'
                              'Raising this value will mean that periods of silence have to be longer before they'
                              'will be removed, and vice versa.')

    if event == 'infoSSkipThresh':
        window['info'].update('The Silence Threshold is the volume that the audio has to'
                              ' go below before it counts as silence.\n\n'
                              "If the silence skipping doesn't appear to be working, try raising this value."
                              " If too much is being skipped (including the beginnings and ends of words) try lowering"
                              " this value.")

    if event == 'infoSSkipKeep':
        window['info'].update('The Keep Silence value tells the program how much'
                              ' silence to keep when silence is being skipped.\n\n'
                              'This helps prevent there being absolutely no silence in the audiobook, which can'
                              ' sound fatiguing.')

    if event == 'infoSSkipStep':
        window['info'].update('The Searching Step value controls how often the program checks to see if the audiobook'
                              ' is silent or not.\n\n'
                              'For example, if Seek Step is set to 5ms, it will check for'
                              ' silence every five milliseconds.\n\n'
                              'The only reason to raise this number is to make the program run quicker.')

    # ---Info Buttons for Export Page
    if event == 'infoExport':
        window['info'].update('Exporting means saving the audiobook as a file other programs can open.'
                              ' Unless you have special requirements, I recommend just clicking "Save As", typing your'
                              ' file name, and then just pressing enter.')

    if event == sg.WIN_CLOSED or event == 'Exit':  # If user closed window with X then exit
        break

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

window.close()
