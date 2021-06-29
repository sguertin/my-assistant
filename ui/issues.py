import PySimpleGUI as sg

def manage_issues(issues):
    window = sg.Window(f'Time Tracking - Add New Entry', [
        [sg.T(f'Please provide the Issue information')],
        [sg.Listbox(['Issue 1', 'Issue 2'], key='ToRemove', size=(25, 65)), sg.Frame('',
            [[sg.Button('+', key='-ADD-')], [sg.Button('-', key='-REMOVE-')]]
        ), sg.Listbox(['Issue 3', 'Issue 4'], key='ToAdd', size=(25, 65))],
        [
            sg.Button('Save and Close', key='Save'), 
            sg.Cancel(),
        ]
    ], size=(500, 750))
    while True:
        event, values = window.read()
        print(f'{event=}, {values=}')
        if event in ('Save', 'Cancel', sg.WINDOW_CLOSED):
            window.close()
            break
