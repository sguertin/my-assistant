import PySimpleGUI as sg

from my_assistant.models.events import Events
from my_assistant.views.view import View


class IssueInformationView(View):
    view: sg.Window
    issue_field: sg.Input
    desc_field: sg.Input
    result_field: sg.Text

    def __init__(self):
        self.issue_field = sg.Input(key="-ISSUE-")
        self.desc_field = sg.Input(key="-DESCRIPTION-")
        self.result_field = sg.Text(
            f"Issue PRODSUP-00000000 was successfully added", visible=False
        )
        self.view = sg.Window(
            f"Time Tracking - Add New Entry",
            [
                [sg.Text(f"Please provide the Issue information")],
                [self.result_field],
                [sg.Text(f"Issue Number: "), self.issue_field],
                [sg.Text(f"Description:  "), self.desc_field],
                [
                    sg.Button(
                        "Save and Add Another", key=Events.ANOTHER, bind_return_key=True
                    ),
                    sg.Button("Save and Close", key=Events.SAVE),
                    sg.Button(Events.CLOSE),
                ],
            ],
        )
