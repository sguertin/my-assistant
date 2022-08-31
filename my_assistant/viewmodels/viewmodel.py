from abc import ABCMeta, abstractmethod


class ViewModel(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "load") and callable(subclass.load)) or NotImplemented

    @abstractmethod
    def load(self, results: dict[str, str]) -> object:
        raise NotImplementedError(self.load)
