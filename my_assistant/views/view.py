from abc import ABCMeta, abstractmethod

import PySimpleGUI as sg


class View(metaclass=ABCMeta):
    view: sg.Window

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "read") and callable(subclass.read)) or NotImplemented

    @abstractmethod
    def read(self, close: bool = True) -> tuple[str, dict[str, str]]:
        return self.view.read(close=close)

    @abstractmethod
    def close(self) -> None:
        self.view.close()
