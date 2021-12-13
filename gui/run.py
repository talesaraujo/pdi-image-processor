import os
import sys
from PySimpleGUI.PySimpleGUI import I; sys.path.insert(1, os.path.join(sys.path[0], '..'))
import numpy as np
import cv2 as cv
import PySimpleGUI as sg

from gui import inputs
from image_processor import ImageContext
from image_processor.core import intensity


ALLOWED_EXTENSIONS = [
    ".bmp",
    "jpg",
    "bmp"
]

BLANK_CANVAS = np.full((768, 1366), 217)

sg.ChangeLookAndFeel('Default1')     
sg.set_options(
    font=("DejaVu Sans", 10),
    element_padding=(0, 0)
)


# ------ Menu Definition ------ #      
menu_def = [
    [ 'File', [ 'Open', 'Save', 'Exit' ] ],
    [ 'Edit', [ 'Clear', 'Undo', 'Paste' ], ],
    [ 'Mode', [ 'RGB', 'Grayscale' ] ],
    [ 'Intensity', [ 'Negative', 'Brightness', 'Log-Transform', 'Gamma-Correction' ] ],
    [ 'Help', 'About'],
]

# ------ GUI Defintion ------ #

frame_layout = [
    [sg.Image(key="IMAGE", size=(1366, 768), pad=(100, 100))]
]

main_layout = [      
    [sg.Menu(menu_def)],
    [sg.Frame(title="", size=(1366, 768), layout=frame_layout, element_justification='c', vertical_alignment='center')]  
]      

main_window = sg.Window(
    "Image-Processor",
    main_layout,
    default_element_size=(12, 1),
    auto_size_text=False,
    auto_size_buttons=False,
    default_button_element_size=(12, 1)
)

icontext = ImageContext()

# ------ Loop & Process button menu choices ------ #      
while True:

    event, values = main_window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    print('Button = ', event)

    # ------ Process menu choices ------ #      
    if event == 'About':      
        sg.popup('Image Processor', 'Version 0.1', 'Created by @talesaraujo')  


    elif event == 'Open':      
        img_path = sg.popup_get_file('File to open', no_window=True)

        if img_path:
            icontext.load_image(img_path)
            main_window["IMAGE"].update(cv.imencode('.png', icontext.image)[1].tobytes())


    elif event == 'Save':      
        img_path = sg.popup_get_folder('Save file to', no_window=True)

        if img_path:
            print(img_path)
    

    elif event == 'Clear':
        icontext.image = None
        main_window["IMAGE"].update(cv.imencode('.png', BLANK_CANVAS)[1].tobytes())


    elif event == 'Undo':
        if icontext.image is not None:
            icontext.undo()
            main_window["IMAGE"].update(cv.imencode('.png', icontext.image)[1].tobytes())
        else:
            sg.popup_quick_message('No previous operations.')


    elif event == 'Grayscale':
        if icontext.image is not None:
            icontext.to_grayscale()

            img_bytes = cv.imencode('.png', icontext.image)[1].tobytes()
            main_window["IMAGE"].update(img_bytes)
        else:
            sg.popup_error('No loaded image to apply effect!')
    

    elif event == 'Negative':
        if icontext.image is not None:
            icontext.normalize()
            icontext.apply_transform(intensity.negative)
            icontext.denormalize()
            main_window["IMAGE"].update(cv.imencode('.png', icontext.image)[1].tobytes())
        
        else:
            sg.popup_error('Error', 'No loaded image to apply effect!')
    

    elif event == 'Brightness':
        if icontext.image is not None:
            factor = sg.popup_get_text('Enter brightness value factor')

            if factor:
                icontext.normalize()
                icontext.apply_transform(intensity.set_brightness, float(factor))
                icontext.denormalize()
                main_window["IMAGE"].update(cv.imencode('.png', icontext.image)[1].tobytes())
            else:
                sg.popup_error("No value set!")
        else:
            sg.popup_error('No loaded image to apply effect!')


    elif event == 'Log-Transform':
        if icontext.image is not None:
            c = sg.popup_get_text('Enter value of c (logarithmic factor)')

            if c:
                icontext.normalize()
                icontext.apply_transform(intensity.log_transform, float(c))
                icontext.denormalize()
                main_window["IMAGE"].update(cv.imencode('.png', icontext.image)[1].tobytes())
            else:
                sg.popup_error("No value set!")
   
        else:
            sg.popup_error('No loaded image to apply effect!')


    elif event == 'Gamma-Correction':
        if icontext.image is not None:
            input_popup = inputs.get_gamma_transform()
            input_event, input_values = input_popup.read()
            input_popup.close()

            if input_event == "Apply":
                # print(input_event)
                c, gamma = input_values[0], input_values[1]

                if c and gamma:
                    icontext.normalize()
                    icontext.apply_transform(intensity.gamma_transform, float(c), float(gamma))
                    icontext.denormalize()
                    main_window["IMAGE"].update(cv.imencode('.png', icontext.image)[1].tobytes())
                else:
                    sg.popup_error("Missing values. Try again")
   
        else:
            sg.popup_error('No loaded image to apply effect!')
