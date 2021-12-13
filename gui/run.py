import os
import sys
from tkinter.constants import ALL; sys.path.insert(1, os.path.join(sys.path[0], '..'))
import numpy as np
import cv2 as cv
import PySimpleGUI as sg

from image_processor import ImageContext, imgio
from image_processor.core import intensity, sampling
from gui import inputs


ALLOWED_EXTENSIONS = [
    ".bmp",
    ".jpg",
    ".png"
]

BLANK_CANVAS = np.full((768, 1366), 240)

sg.ChangeLookAndFeel('Default1')     
sg.set_options(
    font=("Segoe UI", 9),
    element_padding=(0, 0)
)


# ------ Menu Definition ------ #      
menu_def = [
    [ 'File', [ 'Open', 'Save', 'Exit' ] ],
    [ 'Edit', [ 'Clear', 'Undo', 'Paste' ], ],
    [ 'Mode', [ 'RGB', 'Grayscale' ] ],
    [ 'Intensity', [ 'Negative', 'Brightness', 'Log-Transform', 'Gamma-Correction', 'Linear-Interpolation' ] ],
    [ 'Colors', [ 'Equalize Histogram'] ],
    [ 'Filters', ['Generic Convolution', 'Gaussian Blur', 'Average Smoothing', ['Normal', 'Weighted'] , 'Sharpening', [ 'Laplacian', 'High-Boost' ] ]  ],
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
        if icontext.image is not None and icontext.image is not BLANK_CANVAS:
            sv_input_popup = inputs.new_save_input()
            sv_input_event, sv_input_values = sv_input_popup.read()
            sv_input_popup.close()

            filename = sv_input_values[0]
            name, extension = os.path.splitext(filename)
            
            if sv_input_event == 'SAVE-OK' and extension in ALLOWED_EXTENSIONS:
                img_path = sg.popup_get_folder('Select location', no_window=True)
                save_path = os.path.join(os.path.abspath(img_path), filename)
                success = cv.imwrite(save_path, icontext.image)
                if not success:
                    sg.popup_error("Failed to save file!")

            elif sv_input_event == 'SAVE-CANCEL':
                pass

            else:
                sg.popup_error(f"This image processor only supports the following extensions: {ALLOWED_EXTENSIONS}")
            
        else:
            sg.popup_error("There's no image to save!")


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
            # FIXME: It does not work properly when switching mode (color to grayscale)
            # icontext.normalize()
            icontext.to_grayscale()
            # icontext.denormalize()
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
            sg.popup_error("No loaded image to apply effect!")


    elif event == 'Linear-Interpolation':
        if icontext.image is not None:
            li_input_popup = inputs.get_linear_piecewise()
            li_input_event, li_input_values = li_input_popup.read()
            li_input_popup.close()

            if li_input_event == "Apply":
                pa_x, pa_y = li_input_values[0], li_input_values[2]
                pb_x, pb_y = li_input_values[1], li_input_values[3]

                if pa_x and pa_y and pb_x and pb_y:
                    try:
                        icontext.apply_transform(
                            intensity.linear_piecewise,
                            (int(pa_x), int(pa_y)), (int(pb_x), int(pb_y)),
                            True
                        )
                        main_window["IMAGE"].update(cv.imencode('.png', icontext.image)[1].tobytes())
                    except ValueError as v_err:
                        sg.popup_error(v_err)

                else:
                    sg.popup_error('Values are missing. Please try again.')
        else:
            sg.popup_error("No loaded image to apply effect!")
    
    elif event == "Equalize Histogram":
        if icontext.image is not None:
            icontext.apply_transform(sampling.equalize_histogram)
            main_window["IMAGE"].update(cv.imencode('.png', icontext.image)[1].tobytes())
        else:
            sg.popup_error("No loaded image to apply effect!")
