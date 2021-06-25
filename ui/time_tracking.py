from datetime import datetime
import json
from pathlib import Path

import PySimpleGUIQt as sg

from issues import add_issue


def get_entry_info()-> tuple[str, str]:
    issue_field = sg.In(key='-ISSUE-')
    desc_field = sg.In(key='-DESCRIPTION-')
    window = sg.Window(f'Time Tracking',
        [
            [sg.T(f'Please provide the Issue information')],
            [sg.T(f'Issue Number: '), issue_field],
            [sg.T(f'Description: '), desc_field],
            [
                sg.Button('Save and Add Another', key='Another', bind_return_key=True), 
                sg.Button('Save and Close', key='Save'), 
                sg.Cancel('Close')
            ]
        ]
    )    
    while True:
        event, values = window.read()
        issue_num, description = values['-ISSUE-'], values['-DESCRIPTION-']
        if event == 'Cancel' or not issue_num:
            window.close()
            return None, None
        else:
            issue = { 'issue_num': issue_num, 'description': description }
            add_issue(issue)                
            if event == 'Save':
                window.close()
                return f'{issue_num} - {description}'
            elif event == 'Another':
                issue_field.Update('', select=True)
                desc_field.Update('')        
            

def record_time(entries: list[str], now: datetime) -> tuple[str,str]:
    combo = sg.Combo(entries, key='-ENTRY-')
    window = sg.Window(f'Time Tracking',
            [
                [sg.T(f'What have you been working on for {now.hour - 1}:00 - {now.hour}:00?')],
                [combo, sg.Button(button_text='Add Entry', key='AddEntry')],
                [sg.T('Comment (Optional): '), sg.In('-COMMENT-')]
                [sg.Submit('OK'), sg.Cancel('Cancel') ]
            ]
        )
    while True:
        event, values = window.read()
        if event == 'Submit':
            window.close()
            return values['-ENTRY-'], values['-COMMENT-']
        elif event == 'Cancel':
            window.close()
            return None, None
        elif event == 'AddEntry':
            new_issue = get_entry_info()
            entries.append(new_issue)
            combo.Update(values=entries)
