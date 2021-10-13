import time
import numpy as np
import noisereduce as nr
from pydub import (
    AudioSegment,
    silence,
    effects,
    scipy_effects)
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



sg.LOOK_AND_FEEL_TABLE['ABETheme'] = {'BACKGROUND': '#180D2B',
                                      'TEXT': '#FFF3CC',
                                      'INPUT': '#FFFFFF',
                                      'TEXT_INPUT': '#000000',
                                      'SCROLL': '#F3CC49',
                                      'BUTTON': ('#000000', '#F3CC49'),
                                      'PROGRESS': ('#D1826B', '#CC8019'),
                                      'BORDER': 1, 'SLIDER_DEPTH': 0,
                                      'PROGRESS_DEPTH': 0, }

sg.theme('ABETheme')

# --- Setting the fonts
Header = ("Century Schoolbook Bold", 25)
HeaderC = '#F3CC49'
HeaderBG = '#2F1042'

# --- Creating the different pages in the program

# --- Home screen
LOHome = [
    [sg.Text(
        'ㅤ       db        88        88  88888888ba,    88    ,ad8888ba,    88888888ba     ,ad8888ba,      ,ad8888ba,    88      a8P'
        ' ㅤ      d88b       88        88  88      `"8b   88   d8"`    `"8b   88      "8b   d8"`    `"8b    d8"`    `"8b   88    ,88` '
        ' ㅤ     d8``8b      88        88  88        `8b  88  d8`        `8b  88      ,8P  d8`        `8b  d8`        `8b  88  ,88"   '
        ' ㅤ    d8`  `8b     88        88  88         88  88  88          88  88aaaaaa8P`  88          88  88          88  88,d88`    '
        ' ㅤ   d8YaaaaY8b    88        88  88         88  88  88          88  88""""""8b,  88          88  88          88  8888"88,   '
        ' ㅤ  d8""""""""8b   88        88  88         8P  88  Y8,        ,8P  88      `8b  Y8,        ,8P  Y8,        ,8P  88P   Y8b  '
        ' ㅤ d8`        `8b  Y8a.    .a8P  88      .a8P   88   Y8a.    .a8P   88      a8P   Y8a.    .a8P    Y8a.    .a8P   88     "88,'
        ' ㅤd8`          `8b  `"Y8888Y"`   88888888Y"`    88    `"Y8888Y"`    88888888P"     `"Y8888Y"`      `"Y8888Y"`    88       Y8b'
        ' ㅤ                                                                                                                           '
        'ㅤ ㅤ                                                                         ,ad88888888888888888888888888888ba,             '
        ' ㅤ88888888888  888b      88    ,ad8888ba,   88  888b      88  88888888888     d8’                             ‘88            '
        ' ㅤ88           8888b     88   d8"`    `"8b  88  8888b     88  88              88                               88            '
        ' ㅤ88           88 `8b    88  d8`            88  88 `8b    88  88              88      ,d888888888888888b,      88            '
        ' ㅤ88aaaaa      88  `8b   88  88             88  88  `8b   88  88aaaaa         88     dp’  ‘qh      dp’ ‘qb     88            '
        ' ㅤ88"""""      88   `8b  88  88      88888  88  88   `8b  88  88"""""         88     qb.  .dY      Yb.  dp     88            '
        ' ㅤ88           88    `8b 88  Y8,        88  88  88    `8b 88  88              88      ‘Y888888888888888Y’      88            '
        ' ㅤ88           88     `8888   Y8a.    .a88  88  88     `8888  88              88                               88            '
        ' ㅤ88888888888  88      `888    `"Y88888P"   88  88      `888  88888888888     88.   ,888888888888888888888,   ,88            '
        'ㅤ                                                                            ‘Y8888888888888888888888888888888Y’',
        size=(126, 19), font=("Courier New", 7), text_color='#F3CC49')],
    [sg.Text('Choose a file to be processed', justification='center')],
    [sg.InputText(key='-file1-', default_text='C:/Users/Richard/Documents/GitHub/Audiobooks/files/tower.wav'),
     sg.FileBrowse()],
    [sg.Button('Load File', key='NHome')]
]

# ---Default Error Text
ErrorText = 'Something went wrong'

# ---Select Processes Screen
LOProcess = [
    [sg.Text('Choose Processes', size=(20, 1), justification='center', font=Header,
             relief=sg.RELIEF_GROOVE, text_color=HeaderC, background_color=HeaderBG)],
    [sg.Frame('', [
        [sg.Checkbox('Compression', default=False, key="-Comp-")],
        [sg.Checkbox('Normalisation', default=False, key="-Norm-")],
        [sg.Checkbox('Background Noise Reduction', default=False, key="-NR-")],
        [sg.Checkbox('Mouth Noise Reduction', default=False, key="-MNR-")],
        [sg.Checkbox('Vocal EQ', default=False, key="-EQ-")],
        [sg.Checkbox('Silence Skipping', default=False, key="-SSkip-")],
        [sg.Checkbox('Librosa Test', default=False, key="-libtest-")],
    ], element_justification='Left', relief=sg.RELIEF_FLAT)],
    [sg.Button('Next', key='NProcesses')]
]

# --- Compression Screen
LOComp = [
    [sg.Text('Compression', size=(30, 1), justification='center', font=Header,
             relief=sg.RELIEF_GROOVE, text_color=HeaderC, background_color=HeaderBG)],
    [sg.Button('Next', key='NComp')]]

# --- Normalisation Screen
LONorm = [
    [sg.Text('Normalisation', size=(30, 1), justification='center', font=Header,
             relief=sg.RELIEF_GROOVE, text_color=HeaderC, background_color=HeaderBG)],
    [sg.Text('Headroom:', size=(8, 1)), sg.InputText(key="VNorm", size=(4, 1), default_text='-0.5')],
    [sg.Button('Next', key='NNorm')]]

# --- Background Noise Reduction Screen
LONR = [
    [sg.Text('Background Noise Reduction', size=(30, 1), justification='center', font=Header,
             relief=sg.RELIEF_GROOVE, text_color=HeaderC, background_color=HeaderBG)],
    [sg.Button('Next', key='NNR')]]

# --- Mouth Noise Reduction Screen
LOMNR = [
    [sg.Text('Mouth Noise Reduction', size=(30, 1), justification='center', font=Header,
             relief=sg.RELIEF_GROOVE, text_color=HeaderC, background_color=HeaderBG)],
    [sg.Button('Next', key='NMNR')]]

# --- Vocal EQ Screen
LOEQ = [
    [sg.Text('Vocal EQ', size=(32, 1), justification='center', font=Header,
             relief=sg.RELIEF_GROOVE, text_color=HeaderC, background_color=HeaderBG)],
    [sg.InputCombo(('Default', 'Weird'), default_value='Default', size=(20, 1),
                   key='EQcombo',
                   enable_events=True)],
    [sg.Frame('Manual EQ', [
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
    ])],
    [sg.Button('Next', key='NEQ')]]

# --- Silence Skipping Screen
LOSSkip = [
    [sg.Text('Silence Skipping', size=(30, 1), justification='center', font=Header,
             relief=sg.RELIEF_GROOVE, text_color=HeaderC, background_color=HeaderBG)],
    [sg.Button('Next', key='NSSkip')]]

# --- Librosa Test Screen
LOlibtest = [
    [sg.Text('Librosa Test', size=(30, 1), justification='center', font=Header,
             relief=sg.RELIEF_GROOVE, text_color=HeaderC, background_color=HeaderBG)],
    [sg.Button('Next', key='Nlibtest')]]

# --- Export Screen
LOExport = [
    [sg.Text('Export', size=(30, 1), justification='center', font=Header,
             relief=sg.RELIEF_GROOVE, text_color=HeaderC, background_color=HeaderBG)],
    [sg.Button('Next', key='NExport')]]

# --- Error Screen
LOError = [
    [sg.Text(ErrorText, size=(40, 1), justification='center', font=("Helvetica", 15), relief=sg.RELIEF_RIDGE)],
    [sg.Button('Close', key='NError')]
]

# --- Creating the wrapper layout

layout = [[sg.Frame('', [
    [sg.Column(LOHome, key='-LOHome', element_justification='Centre', vertical_alignment='Centre'),
     sg.Column(LOProcess, visible=False, key='-LOProcess', element_justification='Centre', vertical_alignment='Centre'),
     sg.Column(LOComp, visible=False, key='-LOComp', element_justification='Centre'),
     sg.Column(LONorm, visible=False, key='-LONorm', element_justification='Centre'),
     sg.Column(LONR, visible=False, key='-LONR', element_justification='Centre'),
     sg.Column(LOMNR, visible=False, key='-LOMNR', element_justification='Centre'),
     sg.Column(LOEQ, visible=False, key='-LOEQ', element_justification='Centre'),
     sg.Column(LOSSkip, visible=False, key='-LOSSkip', element_justification='Centre'),
     sg.Column(LOlibtest, visible=False, key='-LOlibtest', element_justification='Centre'),
     sg.Column(LOExport, visible=False, key='-LOExport', element_justification='Centre')]
    ], background_color='#180D2B', border_width=10, relief=sg.RELIEF_FLAT, pad=20, element_justification='Center', vertical_alignment='Center')]]

# ---Creating and populating the list of pages (To be added to on the processes page)
Pages = ['-LOHome', '-LOProcess']
Page = 0

# ---Defining Vocal EQ Settings
EQPSDefault = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
EQPSWeird = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
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
                   titlebar_icon=''
                   )

window2 = sg.Window('Error', LOError, finalize=True)
window2.hide()

def errormsg():
    window2.refresh()
    window2.un_hide()
    while True:
        event2, values2 = window2.read()
        if event2 == 'NError':
            break
    window2.hide()


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
        print(values['VNorm'])
        if type(values['VNorm']) == str:
            print('Not String')
            if float(values['VNorm']) > float(0.0):
                ErrorText = 'Please input a negative number'
                errormsg()
            else:
                print("Normalising...")
                ABook = effects.normalize(ABook, headroom=3.2)

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
        bgsamples = BGNoise.get_array_of_samples()
        yNoise = np.array(bgsamples)

        samples = ABook.get_array_of_samples()
        y= np.array(samples)

        # perform noise reduction
        print("Reducing Noise...")
        reduced_noise = nr.reduce_noise(y=y, sr=44100, y_noise=yNoise, prop_decrease=0.5)

        # ---Loads new, shifted file up as ABook
        ABook = ABook._spawn(reduced_noise)

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
        RO = 2

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=32, bandwidth=21, filter_mode="peak",
                                 gain_dB=values['eq32'], order=RO)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=64, bandwidth=43, filter_mode="peak",
                                 gain_dB=values['eq64'], order=RO)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=125, bandwidth=79, filter_mode="peak",
                                 gain_dB=values['eq125'], order=RO)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=250, bandwidth=171, filter_mode="peak",
                                 gain_dB=values['eq250'], order=RO)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=500, bandwidth=329, filter_mode="peak",
                                 gain_dB=values['eq500'], order=RO)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=1000, bandwidth=671, filter_mode="peak",
                                 gain_dB=values['eq1k'], order=RO)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=2000, bandwidth=1329, filter_mode="peak",
                                 gain_dB=values['eq2k'], order=RO)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=4000, bandwidth=2671, filter_mode="peak",
                                 gain_dB=values['eq4k'], order=RO)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=8000, bandwidth=5329, filter_mode="peak",
                                 gain_dB=values['eq8k'], order=RO)

        # --- 32Hz
        ABook = scipy_effects.eq(ABook, focus_freq=16000, bandwidth=10671, filter_mode="peak",
                                 gain_dB=values['eq16k'], order=RO)

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
        time.sleep(1)
        break

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

window.close()