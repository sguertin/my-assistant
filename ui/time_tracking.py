from datetime import datetime
import json

import PySimpleGUIQt as sg

def get_entry_info()-> tuple[str, str]:
    event, values = sg.Window(f'Time Tracking',
        [
            [sg.T(f'Please provide the Issue information')],
            [sg.T(f'Issue Number:'), sg.In(key='-ISSUE-')],
            [sg.T(f'Description:'), sg.In(key='-DESCRIPTION-')],
            [sg.Submit(), sg.Cancel()]
        ]
    ).read(close=True)
    if event == 'Submit':
        issue_num, description = values['-ISSUE-'], values['-DESCRIPTION-']
        if issue_num is None:
            return None
        else:
            file_entry = { 'issue': issue_num, 'description': description }
            with open('entries.json', 'r') as f:
                old_entries: list[dict] = json.loads(f.read())
            old_entries.append(file_entry)
            with open('entries.json', 'w') as f:
                f.write(json.dumps(old_entries))
        return f'{issue_num} - {description}'
    elif event == 'Cancel':
        return None, None

def record_time(entries: list[str], now: datetime) -> str:
    combo = sg.Combo(entries, key='-ENTRY-')
    window = sg.Window(f'Time Tracking',
            [
                [sg.T(f'What have you been working on for {now.hour - 1}:00 - {now.hour}:00?')],
                [combo, sg.Button(button_text='Add Entry', key='AddEntry')],
                [sg.Submit('OK'), sg.Cancel('Cancel') ]
            ]
        )
    while True:
        event, values = window.read()
        if event == 'Submit':
            window.close()
            return values['-ENTRY-']
        elif event == 'Cancel':
            window.close()
            return None
        elif event == 'AddEntry':
            new_issue = get_entry_info()
            entries.append(new_issue)
            combo.Update(values=entries)
