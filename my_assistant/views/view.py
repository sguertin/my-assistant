from abc import ABCMeta, abstractmethod

import PySimpleGUI as sg

from my_assistant.viewmodels.viewmodel import ViewModel


class View(metaclass=ABCMeta):
    window: sg.Window
    viewmodel: ViewModel

    def read(self, close: bool = True) -> tuple[str, dict[str, str] | ViewModel]:
        event, values = self.window.read(close=close)
        if self.viewmodel:
            return event, self.viewmodel.load(values)
        return event, values

    def close(self) -> None:
        self.window.close()
