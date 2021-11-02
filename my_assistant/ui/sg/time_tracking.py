from datetime import datetime
from typing import Callable

import PySimpleGUI as sg

from my_assistant.models.issues import Issue
from my_assistant.services.issues import get_issues_list
from my_assistant.ui.sg.issues import manage_issues


def record_time(timestamp: datetime, handle_update_issues: Callable[[], list[Issue]]) -> tuple[Issue, str]:
    entries = get_issues_list()
    combo = sg.Combo(entries, key='-ENTRY-')
    window = sg.Window(f'Time Tracking', [
        [sg.T(
            f'What have you been working on for {timestamp.hour - 1}:00 - {timestamp.hour}:00?')],
        [combo, sg.Button(button_text='Manage Issues',
                          key='ManageIssues')],
        [sg.T('Comment (Optional): '), sg.In(key='-COMMENT-')],
        [sg.Submit(), sg.Button('Skip'), sg.Button('Refresh')],
    ]
    )
    while True:
        event, values = window.read()

        if event == 'Submit':
            window.close()
            return values['-ENTRY-'], values['-COMMENT-']
        elif event in ('Skip', sg.WINDOW_CLOSED):
            window.close()
            return None, None
        elif event == 'ManageIssues':
            new_issues = handle_update_issues()
            combo.Update(new_issues)

        window.refresh()
