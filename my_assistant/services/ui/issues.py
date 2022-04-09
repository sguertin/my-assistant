from logging import Logger

import PySimpleGUI as sg

from my_assistant.interfaces.issues import IIssueService
from my_assistant.interfaces.logfactory import ILoggingFactory
from my_assistant.interfaces.ui.warning import IUIWarningService
from my_assistant.models.issues import Issue


class UIIssueService:
    issue_service: IIssueService
    ui_warning_service: IUIWarningService
    log: Logger

    def __init__(
        self,
        issue_service: IIssueService,
        ui_warning_service: IUIWarningService,
        log_factory: ILoggingFactory,
    ):
        self.issue_service = issue_service
        self.ui_warning_service = ui_warning_service
        self.log = log_factory.get_logger("UIIssueService")

    def get_issue_info(self, issues: list[Issue]) -> list[Issue]:
        issue_field = sg.In(key="-ISSUE-")
        desc_field = sg.In(key="-DESCRIPTION-")
        result_field = sg.T(
            f"Issue PRODSUP-00000000 was successfully added", visible=False
        )
        window = sg.Window(
            f"Time Tracking - Add New Entry",
            [
                [sg.T(f"Please provide the Issue information")],
                [result_field],
                [sg.T(f"Issue Number: "), issue_field],
                [sg.T(f"Description:  "), desc_field],
                [
                    sg.Button(
                        "Save and Add Another", key="Another", bind_return_key=True
                    ),
                    sg.Button("Save and Close", key="Save"),
                    sg.Button("Close"),
                ],
            ],
        )
        while True:
            event, values = window.read()
            self.log.info("Event %s received", event)
            if event in ("Another", "Save") and values:
                issue_num, description = values["-ISSUE-"], values["-DESCRIPTION-"]
                if issue_num:
                    issue = Issue(issue_num, description)
                    self.issue_service.add_issue(issue)
                    issues.append(issue)
                    window.refresh()
                if event == "Save":
                    window.close()
                    break
                elif event == "Another":
                    result_field.update(
                        f"Issue {issue_num} was successfully added", visible=True
                    )
                    issue_field.Update("", select=True)
                    desc_field.Update("")
                    window.refresh()
            else:
                window.close()
                break
        return issues

    def manage_issues(self) -> tuple[bool, list[Issue]]:
        has_changes = False
        issues = self.issue_service.get_issues_list()
        deleted_issues = self.issue_service.get_deleted_issues()
        active_list_box = sg.Listbox(issues, key="ActiveIssues", size=(30, 40))
        deleted_list_box = sg.Listbox(
            deleted_issues, key="DeletedIssues", size=(30, 40)
        )
        window = sg.Window(
            f"Time Tracking - Manage Issues",
            [
                [
                    sg.T("Active Issues", size=(30, 1)),
                    sg.T("", size=(5, 1)),
                    sg.T("Deleted Issues", size=(30, 1)),
                ],
                [
                    active_list_box,
                    sg.Frame(
                        "",
                        [
                            [
                                sg.Button(
                                    " + ",
                                    key="-ADD-",
                                    size=(5, 1),
                                    tooltip="Add New Issue",
                                )
                            ],
                            [
                                sg.Button(
                                    " <- ",
                                    key="-RESTORE-",
                                    size=(5, 1),
                                    tooltip="Restore Selected Issues",
                                )
                            ],
                            [
                                sg.Button(
                                    " -> ",
                                    key="-REMOVE-",
                                    size=(5, 1),
                                    tooltip="Delete Selected Issues",
                                )
                            ],
                        ],
                    ),
                    deleted_list_box,
                ],
                [
                    sg.Button("Save and Close", key="Save"),
                    sg.Cancel(),
                ],
            ],
            size=(550, 775),
        )
        while True:
            event, values = window.read()
            if event == "-ADD-":
                issues = self.get_issue_info(issues)
                active_list_box.update(issues)
                has_changes = True
            elif event == "-REMOVE-":
                for issue in values["ActiveIssues"]:
                    issues.remove(issue)
                    deleted_issues.append(issue)
                has_changes = True
            elif event == "-RESTORE-":
                for issue in values["DeletedIssues"]:
                    deleted_issues.remove(issue)
                    issues.append(issue)
                has_changes = True
            if event == "Save":
                self.issue_service.save_issues_list(issues, deleted_issues)
                window.close()
                break
            elif (
                event in ("Cancel", sg.WINDOW_CLOSE_ATTEMPTED_EVENT) and not has_changes
            ):
                window.close()
                break
            elif event in ("Cancel", sg.WINDOW_CLOSE_ATTEMPTED_EVENT) and has_changes:
                proceed = self.ui_warning_service.warning_ok_cancel_prompt(
                    "None of your changes have been saved, are you sure want to continue?"
                )
                if proceed:
                    window.close()
                    break
            else:
                active_list_box.update(issues)
                deleted_list_box.update(deleted_issues)
            return event == "Save", issues
