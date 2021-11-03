import logging
from logging import Logger
from typing import Any, Callable, Optional

from my_assistant.interfaces.ui import IUIProvider


class MockUIProvider(IUIProvider):
    log: Logger

    def __init__(self,
                 change_settings: Optional[Callable] = None,
                 credentials_prompt: Optional[Callable] = None,
                 get_issue_info: Optional[Callable] = None,
                 manage_issues: Optional[Callable] = None,
                 manage_theme: Optional[Callable] = None,
                 record_time: Optional[Callable] = None,
                 warning_ok_cancel_prompt: Optional[Callable] = None,
                 warning_prompt: Optional[Callable] = None,
                 warning_retry_prompt: Optional[Callable] = None):
        log = logging.getLogger('MockTrackingService')
        self.change_settings = lambda *args: self.log_args(
            log, args=tuple(args), method='change_settings', callback=change_settings)
        self.credentials_prompt = lambda *args: self.log_args(
            log, args=tuple(args), method='credentials_prompt', callback=credentials_prompt)
        self.get_issue_info = lambda *args: self.log_args(
            log, args=tuple(args), method='get_issue_info', callback=get_issue_info)
        self.manage_issues = lambda *args: self.log_args(
            log, args=tuple(args), method='manage_issues', callback=manage_issues)
        self.manage_theme = lambda *args: self.log_args(
            log, args=tuple(args), method='manage_theme', callback=manage_theme)
        self.record_time = lambda *args: self.log_args(
            log, args=tuple(args), method='record_time', callback=record_time)
        self.warning_ok_cancel_prompt = lambda *args: self.log_args(
            log, args=tuple(args), method='warning_ok_cancel_prompt', callback=warning_ok_cancel_prompt)
        self.warning_prompt = lambda *args: self.log_args(
            log, args=tuple(args), method='warning_prompt', callback=warning_prompt)
        self.warning_retry_prompt = lambda *args: self.log_args(
            log, args=tuple(args), method='warning_retry_prompt', callback=warning_retry_prompt)

    @staticmethod
    def log_args(log: Logger, args: tuple[Any], method: str, callback: Callable[[Any], Any] = None):
        arg_text = ", ".join(args)
        log.debug(f'METHOD INVOCATION: {method}({arg_text})')
        if callback:
            result = callback(args)
            if result:
                result = ", ".join(tuple(result))
                log.debug(f'METHOD INVOCATION RESULT: {result}')
                return result
        return None
