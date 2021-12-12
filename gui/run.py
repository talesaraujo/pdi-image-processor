import os
import sys
from PySimpleGUI.PySimpleGUI import I; sys.path.insert(1, os.path.join(sys.path[0], '..'))
import numpy as np
import cv2 as cv
import PySimpleGUI as sg

from image_processor import ImageContext
from image_processor.core import intensity


ALLOWED_EXTENSIONS = [
    ".bmp",
    "jpg",
    "bmp"
]

BLANK_CANVAS = np.full((600, 800), 128)

sg.ChangeLookAndFeel('DarkGrey13')      
sg.set_options(
    font=("DejaVu Sans", 10),
    element_padding=(0, 0)
)


# ------ Menu Definition ------ #      
menu_def = [
    [ 'File', [ 'Open', 'Save', 'Exit' ] ],
    [ 'Edit', [ 'Clear', 'Undo', 'Paste' ], ],
    [ 'Mode', [ 'RGB', 'Grayscale' ] ],
    [ 'Intensity', [ 'Negative', 'Brightness', 'Log Transform', 'Gamma Transform' ] ],
    [ 'Help', 'About'],
]

# ------ GUI Defintion ------ #      
layout = [      
    [sg.Menu(menu_def)],
    [sg.Image(key="IMAGE", size=(800, 600), background_color="gray")],  
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
        window["IMAGE"].update(cv.imencode('.png', icontext.image)[1].tobytes())
    

    elif event == 'Clear':
        icontext.image = None
        window["IMAGE"].update(cv.imencode('.png', BLANK_CANVAS)[1].tobytes())


    elif event == 'Grayscale':
        if icontext.image is not None:
            icontext.to_grayscale()

            img_bytes = cv.imencode('.png', icontext.image)[1].tobytes()
            window["IMAGE"].update(img_bytes)
        else:
            sg.popup_error('No loaded image to apply effect!')
    

    elif event == 'Negative':
        if icontext.image is not None:
            icontext.apply_transform(intensity.negative)
            window["IMAGE"].update(cv.imencode('.png', icontext.image)[1].tobytes())
        
        else:
            sg.popup_error('Error', 'No loaded image to apply effect!')
    

    elif event == 'Brightness':
        if icontext.image is not None:
            factor = float(sg.popup_get_text('Enter brightness value'))
            icontext.apply_transform(intensity.set_brightness, factor)
            window["IMAGE"].update(cv.imencode('.png', icontext.image)[1].tobytes())
            
            if not factor:
                sg.popup_error("No value set!")
        
        else:
            sg.popup_error('No loaded image to apply effect!')