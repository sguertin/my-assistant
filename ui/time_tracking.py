from datetime import datetime

import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import WIN_CLOSED

from issues import add_issue

def get_entry_info(entries: list):
    issue_field = sg.In(key='-ISSUE-')
    desc_field = sg.In(key='-DESCRIPTION-')
    result_field = sg.T(f'                                        ', visible=False)    
    window = sg.Window(f'Time Tracking - Add New Entry', [
            [sg.T(f'Please provide the Issue information')],
            [result_field],
            [sg.T(f'Issue Number: '), issue_field],
            [sg.T(f'Description: '), desc_field],
            [
                sg.Button('Save and Add Another', key='Another', bind_return_key=True), 
                sg.Button('Save and Close', key='Save'), 
                sg.Button('Close')
            ]
        ]
    )    
    while True:
        event, values = window.read()        
        if event in ('Another', 'Save') and values:
            issue_num, description = values['-ISSUE-'], values['-DESCRIPTION-']
            if issue_num:
                issue = { 'issue_num': issue_num, 'description': description }
                entries.append(add_issue(issue))            
            if event == 'Save':
                window.close()
                break
            elif event == 'Another':
                result_field.update(f'Issue {issue_num} was successfully added', visible=True)
                issue_field.Update('', select=True)
                desc_field.Update('')        
        else:
            window.close()
            break

def record_time(entries: list[str], timestamp: datetime) -> tuple[str,str]:
    combo = sg.Combo(entries, key='-ENTRY-')
    window = sg.Window(f'Time Tracking', [
            [sg.T(f'What have you been working on for {timestamp.hour - 1}:00 - {timestamp.hour}:00?')],
            [combo, sg.Button(button_text='Add Entry', key='AddEntry')],
            [sg.T('Comment (Optional): '), sg.In(key='-COMMENT-')],
            [sg.Submit(), sg.Cancel('Cancel') ],
        ]
    )
    while True:        
        event, values = window.read()
        if event == 'Submit':
            window.close()
            return values['-ENTRY-'], values['-COMMENT-']
        elif event in ('Cancel', sg.WIN_CLOSED):
            window.close()
            return None, None
        elif event == 'AddEntry':
            get_entry_info(entries)
            combo.Update(values=entries)
