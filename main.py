from my_assistant.constants import LogLevel
from my_assistant.factories.dependencies import DependencyFactory
from my_assistant.factories.logfactory import LoggingFactory
from my_assistant.interfaces.factories.dependencies import IDependencyFactory
from my_assistant.interfaces.ui.launcher import IUILauncherService
from my_assistant.services.ui.launcher import UILauncherService

log = LoggingFactory(LogLevel.INFO).get_logger("Main")

dependency_factory: IDependencyFactory = DependencyFactory()
try:
    log.info("Starting My Assistant...")
    assistant, ui_provider, settings_service = dependency_factory.create_dependencies()
    launcher: IUILauncherService = UILauncherService(
        assistant, ui_provider, dependency_factory, settings_service
    )
    launcher.run_main_window()
    log.info("Closing My Assistant...")
except Exception as e:
    log.error(e)
