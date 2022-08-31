from my_assistant.constants import LogLevel
from my_assistant.factories.dependencies import DependencyFactory
from my_assistant.factories.log_factory import LoggingFactory
from my_assistant.interfaces.dependency_factory import IDependencyFactory
from my_assistant.interfaces.ui_launcher import IUILauncherService

log = LoggingFactory(LogLevel.INFO).get_logger("Main")

dependency_factory: IDependencyFactory = DependencyFactory()
try:
    log.info("Starting My Assistant...")
    launcher: IUILauncherService = dependency_factory.create_launcher()
    launcher.run_main_window()
    log.info("Closing My Assistant...")
except Exception as e:
    log.error(e)
