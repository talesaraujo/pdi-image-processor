import PySimpleGUI as sg

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
