from abc import ABCMeta, abstractmethod

import PySimpleGUI as sg

from my_assistant.viewmodels.viewmodel import ViewModel


class View(metaclass=ABCMeta):
    view: sg.Window
    viewmodel: ViewModel

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "read") and callable(subclass.read)) or NotImplemented

    @abstractmethod
    def read(self, close: bool = True) -> tuple[str, dict[str, str] | object]:
        event, values = self.view.read(close=close)
        if self.viewmodel:
            return event, self.viewmodel.load(values)
        return event, values

    @abstractmethod
    def close(self) -> None:
        self.view.close()
