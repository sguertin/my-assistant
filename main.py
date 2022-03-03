from os import mkdir
from models.settings import Settings

from my_assistant.constants import WORKING_DIR, ISSUES_LIST, DELETED_ISSUES_LIST, SETTINGS_FILE, LogLevel
from my_assistant.factories.dependencies import DependencyFactory
from my_assistant.factories.logging import LoggingFactory

from my_assistant.services.ui.launcher import LauncherService

log = LoggingFactory(LogLevel.INFO).get_logger('Main')

if not WORKING_DIR.exists():
    log.info(f'Working directory not found at {WORKING_DIR}, creating...')
    mkdir(str(WORKING_DIR))

if not ISSUES_LIST.exists():
    log.info(f'Issues list not found, creating new list')
    with open(ISSUES_LIST, 'w') as f:
        f.write('[]')

if not DELETED_ISSUES_LIST.exists():
    with open(DELETED_ISSUES_LIST, 'w') as f:
        f.write('[]')

if not SETTINGS_FILE.exists():
    with open(SETTINGS_FILE, 'w') as f:
        f.write(Settings().to_json())


try:
    assistant, ui_provider, settings = DependencyFactory.create_dependencies()
    launcher = LauncherService(assistant, ui_provider, settings)
    launcher.run_main_window(lambda: DependencyFactory.create_dependencies())
except Exception as e:
    log.error(e)
