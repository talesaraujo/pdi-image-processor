import os
import sys; sys.path.insert(1, os.path.join(sys.path[0], '..'))
import cv2 as cv
import PySimpleGUI as sg
from image_processor import ImageContext


ALLOWED_EXTENSIONS = [
    ".bmp",
    "jpg",
    "bmp"
]

sg.ChangeLookAndFeel('DarkGrey13')      
sg.set_options(
    font=("Roboto", 12),
    element_padding=(0, 0)
)


# ------ Menu Definition ------ #      
menu_def = [
    ['File', ['Open', 'Save', 'Exit'  ]],
    ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
    ['Intensity', ['Negative', 'Brightness', 'Log Transform', 'Gamma Transform']],
    ['Help', 'About'], ]

# ------ GUI Defintion ------ #      
layout = [      
    [sg.Menu(menu_def)],
    [sg.Image(key="-IMAGE-", size=(800, 600), background_color="gray")],  
]      

window = sg.Window(
    "Image-Processor",
    layout,
    default_element_size=(12, 1),
    auto_size_text=False,
    auto_size_buttons=False,
    default_button_element_size=(12, 1)
)


icontext = ImageContext()

# ------ Loop & Process button menu choices ------ #      
while True:      
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':      
        break      
    print('Button = ', event)

    # ------ Process menu choices ------ #      
    if event == 'About':      
        sg.popup('About this program', 'Version 0.1', 'PySimpleGUI rocks...')  
        
    elif event == 'Open':      
        img_path = sg.popup_get_file('File to open', no_window=True)
        
        icontext.load_image(img_path)
        # # Read image with opencv
        # img = cv.imread(img_path, cv.IMREAD_COLOR)

        # print(type(img))
        # print(img)
        # # Encode img file
        img_bytes = cv.imencode('.png', icontext.image)[1].tobytes()

        window["-IMAGE-"].update(img_bytes)


