from datetime import datetime
from typing import Callable, Any

from my_assistant.interfaces.ui import IUIProvider

from my_assistant.models.issues import Issue
from my_assistant.models.settings import Settings

from my_assistant.ui.sg.credentials import credentials_prompt
from my_assistant.ui.sg.issues import manage_issues, get_issue_info
from my_assistant.ui.sg.settings import change_settings
from my_assistant.ui.sg.theme_browser import manage_theme
from my_assistant.ui.sg.time_tracking import record_time
from my_assistant.ui.sg.warning import warning_ok_cancel_prompt, warning_prompt, warning_retry_prompt


class UIProvider(IUIProvider):
    def __init__(self):
        self.change_settings = change_settings
        self.warning_prompt = warning_prompt
        self.record_time = record_time
        self.credentials_prompt = credentials_prompt
        self.warning_retry_prompt = warning_retry_prompt
        self.manage_issues = manage_issues
        self.manage_theme = manage_theme
        self.get_issue_info = get_issue_info
        self.warning_ok_cancel_prompt = warning_ok_cancel_prompt
