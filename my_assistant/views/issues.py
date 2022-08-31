import PySimpleGUI as sg

from my_assistant.models.events import Events
from my_assistant.viewmodels.issues import IssueInformationKeys, IssueInformationViewModel
from my_assistant.views.view import View


class IssueInformationView(View):
    window: sg.Window

    def __init__(self):        
        self.viewmodel = IssueInformationViewModel()
        self.window = sg.Window(
            f"Time Tracking - Add New Entry",
            [
                [sg.Text(f"Please provide the Issue information")],
                [sg.Text(
                    f"Issue PRODSUP-00000000 was successfully added", key=IssueInformationKeys.RESULT, visible=False
                )],
                [sg.Text(f"Issue Number: "), sg.Input(key=IssueInformationKeys.ISSUE)],
                [sg.Text(f"Description:  "), sg.Input(key=IssueInformationKeys.DESCRIPTION)],
                [
                    sg.Button("Save", key=Events.ANOTHER, bind_return_key=True),
                    sg.Button("Save and Close", key=Events.SAVE),
                    sg.Button(Events.CLOSE),
                ],
            ],
        )
    def reset(self):
        self.set("", "", "")

    def set(
        self, issue_text: str, desc_text: str, result_text: str
    ) -> None:        
        result_visible = (result_text != "" and result_text is not None)
        self.window[IssueInformationKeys.ISSUE].update(issue_text)
        self.window[IssueInformationKeys.DESCRIPTION].update(desc_text)
        self.window[IssueInformationKeys.RESULT].update(result_text, visible=result_visible)
        