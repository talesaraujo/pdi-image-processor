import PySimpleGUI as sg      
import cv2 as cv

sg.ChangeLookAndFeel('Dark')      
sg.set_options(
    # font=("Roboto", 12),
    element_padding=(0, 0)
)

# print(sg.get_opt)

# sg.DEFAULT_FONT = ("Segoe UI Variable", 11)


# ------ Menu Definition ------ #      
menu_def = [
    ['File',['Open', 'Save', 'Exit'  ]],      
    ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],      
    ['Help', 'About'], ]      

# ------ GUI Defintion ------ #      
layout = [      
    [sg.Menu(menu_def, font=("Inter", 10))],     
    [sg.Output(size=(60, 20))],
    # [sg.Image(source=None)]
]      

window = sg.Window(
    "Windows-like program",
    layout,
    default_element_size=(12, 1),
    auto_size_text=False,
    auto_size_buttons=False,
    default_button_element_size=(12, 1)
)

def display_image():
    elements = [
        [sg.Image]
    ]

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
        img_path = sg.popup_get_file('file to open', no_window=True)      
        
        img = cv.imread(img_path, cv.IMREAD_COLOR)
        print(img)

    