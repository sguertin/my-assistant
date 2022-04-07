from os import mkdir

from my_assistant.constants import (
    WORKING_DIR,
    ISSUES_LIST,
    DELETED_ISSUES_LIST,
    SETTINGS_FILE,
)
from my_assistant.factories.dependencies import DependencyFactory
from my_assistant.factories.logfactory import LoggingFactory
from my_assistant.interfaces.factories.dependencies import IDependencyFactory
from my_assistant.models.settings import Settings
from my_assistant.services.ui.launcher import LauncherService

log = LoggingFactory(Settings.load()).get_logger("Main")

if not WORKING_DIR.exists():
    log.info(f"Working directory not found at {WORKING_DIR}, creating...")
    mkdir(str(WORKING_DIR))

if not ISSUES_LIST.exists():
    log.info(f"Issues list not found, creating new list")
    with open(ISSUES_LIST, "w") as f:
        f.write("[]")

if not DELETED_ISSUES_LIST.exists():
    with open(DELETED_ISSUES_LIST, "w") as f:
        f.write("[]")

if not SETTINGS_FILE.exists():
    with open(SETTINGS_FILE, "w") as f:
        f.write(Settings().to_json())

dependency_factory: IDependencyFactory = DependencyFactory()
try:
    assistant, ui_provider, settings = dependency_factory.create_dependencies()
    launcher = LauncherService(assistant, ui_provider, dependency_factory, settings)
    launcher.run_main_window()
except Exception as e:
    log.error(e)
