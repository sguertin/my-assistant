from typing import Callable
import PySimpleGUI as sg

from my_assistant.events import ANOTHER_EVENT, CANCEL_EVENT, CLOSE_EVENT, CLOSE_EVENTS, ADD_EVENT, RESTORE_EVENT, REMOVE_EVENT, SAVE_EVENT, START_UP_EVENT
from my_assistant.models.issues import Issue


ISSUE_KEY: str = '-ISSUE-'
DESCRIPTION_KEY: str = '-DESCRIPTION-'
ACTIVE_ISSUES_KEY: str = '-ACTIVE ISSUES-'
INACTIVE_ISSUES_KEY: str = '-INACTIVE ISSUES-'


def get_issue_info(self, event_handler: Callable[[str, str, str], str]) -> None:
    """Creates UI control to capture issue information and add to list

    Args:
        issues (list[Issue]): The current list of issues
        event_handler (Callable[[str, dict], bool]): The handler for responding to input
    """
    issue_field = sg.Input(key=ISSUE_KEY)
    desc_field = sg.Input(key=DESCRIPTION_KEY)
    result_field = sg.Text(
        f'Issue PRODSUP-00000000 was successfully added', visible=False)
    window = sg.Window(f'Time Tracking - Add New Entry', [
        [sg.T(f'Please provide the Issue information')],
        [result_field],
        [sg.T(f'Issue Number: '), issue_field],
        [sg.T(f'Description:  '), desc_field],
        [
            sg.Button('Save and Add Another',
                      key=ANOTHER_EVENT, bind_return_key=True),
            sg.Button('Save and Close', key=SAVE_EVENT),
            sg.Button('Close', key=CLOSE_EVENT)
        ]
    ])
    event = START_UP_EVENT
    while event not in CLOSE_EVENTS:
        if event != START_UP_EVENT:
            result_field.update(event, visible=True)
            window.refresh()
        event, values = window.read()
        event = event_handler(
            event,
            values[ISSUE_KEY],
            values[DESCRIPTION_KEY]
        )
        issue_field.Update('', select=True)
        desc_field.Update('')

    window.close()


def manage_issues(self,
                  issues: list[Issue],
                  deleted_issues: list[Issue],
                  event_handler: Callable[[str, list[Issue], list[Issue]], tuple[list[Issue], list[Issue]]]) -> list[Issue]:
    active_list_box = sg.Listbox(issues, key=ACTIVE_ISSUES_KEY, size=(30, 40))
    deleted_list_box = sg.Listbox(
        deleted_issues, key=INACTIVE_ISSUES_KEY, size=(30, 40))
    window = sg.Window(f'Time Tracking - Manage Issues', [
        [sg.T('Active Issues', size=(30, 1)), sg.T('', size=(5, 1)),
         sg.T('Inactive Issues', size=(30, 1))],
        [  # CLOSE_EVENTS, SAVE_EVENT, ANOTHER_EVENT, RESTORE_EVENT
            active_list_box,
            sg.Frame('', [
                [sg.Button(' + ', key=ADD_EVENT, size=(5, 1),
                           tooltip='Add New Issue')],
                [sg.Button(' <- ', key=RESTORE_EVENT, size=(5, 1),
                           tooltip='Restore Selected Issues')],
                [sg.Button(' -> ', key=REMOVE_EVENT, size=(5, 1),
                           tooltip='Delete Selected Issues')]
            ]),
            deleted_list_box
        ],
        [
            sg.Button('Save and Close', key=SAVE_EVENT),
            sg.Cancel(key=CANCEL_EVENT),
        ]
    ], size=(550, 775))
    while True:
        event, values = window.read()
        issues = event_handler(
            event, values[ACTIVE_ISSUES_KEY], values[INACTIVE_ISSUES_KEY])
        if not issues:
            window.close()
            break
        else:
            active_list_box.update(issues)
            deleted_list_box.update(deleted_issues)
    return issues
