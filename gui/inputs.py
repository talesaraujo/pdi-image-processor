import PySimpleGUI as sg

def new_save_input():
    return sg.Window(
        title='Export file as',
        layout=[
            [sg.Text('Filename:'), sg.Input()], 
            [sg.OK(key='SAVE-OK'), sg.Cancel(key='SAVE-CANCEL')],
        ],
        element_justification='c'
    )


def get_gamma_transform():
    return sg.Window(
        title="Set gamma correction values",
        layout=[
            [sg.Text("Please enter the values to apply gamma correction:")],
            [sg.Text("c (multiplier factor)", size=(25, 1)), sg.InputText()],
            [sg.Text("gamma (exponent factor)", size=(25, 1)), sg.InputText()],
            [sg.Submit(button_text="Apply"), sg.Cancel()]
        ],
        element_justification='c'
    )

def get_linear_piecewise():
    return sg.Window(
        title="Setting linear piecewise plot points",
        layout=[
            [sg.Text("Set the interpolation points to draw a custom intensity linear function")],
            [sg.Text("Point A (x value):", size=(15,1), border_width=2), sg.Input(pad=20), sg.Text("Point B (x value):", size=(15,1), border_width=2), sg.Input(pad=20)],
            [sg.Text("Point A (y value):", size=(15,1), border_width=2), sg.Input(pad=20), sg.Text("Point B (y value):", size=(15,1), border_width=2), sg.Input(pad=20)],
            [sg.Submit(button_text="Apply"), sg.Cancel()]
        ],
        element_justification='c',
    )


def get_frequency_filter_stats():
    return sg.Window(
        title="Circular filter properties",
        element_justification='c',
        layout=[
            [sg.Text("Please set the range of the circular filter to have frequency cut off")],
            [sg.Text("Radius Size: ", size=(15,1)), sg.Input(pad=20)],
            [sg.Checkbox('Use gaussian filter', default=False)],
            [sg.Submit(button_text="Apply"), sg.Cancel()]
        ]
    )