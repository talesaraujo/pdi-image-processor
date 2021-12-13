import PySimpleGUI as sg

def get_gamma_transform():
    return sg.Window(
        title="Set gamma correction values",
        layout=[
            [sg.Text("Please enter the values to apply gamma correction:")],
            [sg.Text("c (multiplier factor)", size =(25, 1)), sg.InputText()],
            [sg.Text("gamma (exponent factor)", size =(25, 1)), sg.InputText()],
            [sg.Submit(button_text="Apply"), sg.Cancel()]
        ],
        element_justification='c'
    )
