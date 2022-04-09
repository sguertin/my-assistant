from datetime import datetime
from logging import Logger

import PySimpleGUI as sg
from my_assistant.interfaces.issues import IIssueService
from my_assistant.interfaces.factories.log_factory import ILoggingFactory
from my_assistant.interfaces.ui.issues import IUIIssueService
from my_assistant.interfaces.ui.time_tracking import IUITimeTrackingService

from my_assistant.models.issues import Issue


class UITimeTrackingService(IUITimeTrackingService):
    log: Logger

    def __init__(
        self,
        issue_service: IIssueService,
        ui_issue_service: IUIIssueService,
        log_factory: ILoggingFactory,
    ):
        self.issue_service = issue_service
        self.ui_issue_service = ui_issue_service
        self.log = log_factory.get_logger("UITimeTrackingService")

    def record_time(self, timestamp: datetime) -> tuple[Issue, str]:
        entries = self.issue_service.get_issues_list()
        combo = sg.Combo(entries, key="-ENTRY-")
        window = sg.Window(
            f"Time Tracking",
            [
                [
                    sg.T(
                        f"What have you been working on for {timestamp.hour - 1}:00 - {timestamp.hour}:00?"
                    )
                ],
                [combo, sg.Button(button_text="Manage Issues", key="ManageIssues")],
                [sg.T("Comment (Optional): "), sg.In(key="-COMMENT-")],
                [sg.Submit(), sg.Button("Skip"), sg.Button("Refresh")],
            ],
        )
        while True:
            event, values = window.read()
            self.log.info("Event %s received", event)
            if event == "Submit":
                window.close()
                return values["-ENTRY-"], values["-COMMENT-"]
            elif event in ("Skip", sg.WINDOW_CLOSED):
                window.close()
                return None, None
            elif event == "ManageIssues":
                self.ui_issue_service.manage_issues(combo)

            window.refresh()
