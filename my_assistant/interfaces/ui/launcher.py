from abc import abstractmethod, ABCMeta


class ILauncherService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "run_main_window") and callable(subclass.run_main_window)
        ) or NotImplemented

    @abstractmethod
    def run_main_window(self) -> None:
        """Generates the Launcher UI and initiates the application life cycle"""
        raise NotImplementedError()
