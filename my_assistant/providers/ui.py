from datetime import datetime
from typing import Callable, Any

from my_assistant.interfaces.ui import IUIProvider

from my_assistant.models.issues import Issue
from my_assistant.models.settings import Settings

from my_assistant.ui.credentials import credentials_prompt
from my_assistant.ui.issues import manage_issues, get_issue_info
from my_assistant.ui.settings import change_settings
from my_assistant.ui.theme_browser import manage_theme
from my_assistant.ui.time_tracking import record_time
from my_assistant.ui.warning import warning_ok_cancel_prompt, warning_prompt, warning_retry_prompt


class UIProvider(IUIProvider):
    def __init__(self,
                 change_settings: Callable[[IUIProvider, Settings], Settings],
                 credentials_prompt: Callable[[IUIProvider], tuple[str, str]],
                 get_issue_info: Callable[[IUIProvider, Callable[[str, dict], bool]], None],
                 manage_issues: Callable[[[IUIProvider], list[Issue], list[Issue], Callable[[str, dict], tuple[list[Issue], list[Issue]]]],  list[Issue]],
                 manage_theme: Callable[[IUIProvider, Settings], Settings],
                 record_time: Callable[[IUIProvider, datetime], tuple[Issue, str]],
                 warning_ok_cancel_prompt: Callable[[IUIProvider, str], bool],
                 warning_prompt: Callable[[IUIProvider, str], None],
                 warning_retry_prompt: Callable[[IUIProvider, str], bool]
                 ):
        self.change_settings = change_settings
        self.warning_prompt = warning_prompt
        self.record_time = record_time
        self.credentials_prompt = credentials_prompt
        self.warning_retry_prompt = warning_retry_prompt
        self.manage_issues = manage_issues
        self.manage_theme = manage_theme
        self.get_issue_info = get_issue_info
        self.warning_ok_cancel_prompt = warning_ok_cancel_prompt


def get_default_ui_provider() -> IUIProvider:
    return UIProvider(
        change_settings,
        credentials_prompt,
        get_issue_info,
        manage_issues,
        manage_theme,
        record_time,
        warning_ok_cancel_prompt,
        warning_prompt,
        warning_retry_prompt
    )
