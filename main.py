import logging
import logging.config
from os import mkdir

from my_assistant.constants import WORKING_DIR, ISSUES_LIST, DELETED_ISSUES_LIST, SETTINGS_FILE
from my_assistant.interfaces.launcher import ILauncherService
from my_assistant.models.settings import Settings
from my_assistant.providers.dependencies import Factory


logging.basicConfig(
    level=logging.CRITICAL,  # Keeps logging in 3rd party packages quiet
    format='%(name)-15s %(message)s',
    datefmt='[%Y-%m-%d %H:%M:%S]',
)
log = logging.getLogger('ui_assistant.main')
log.setLevel(logging.ERROR)

if not WORKING_DIR.exists():
    mkdir(str(WORKING_DIR))

if not SETTINGS_FILE.exists():
    settings = Settings.restore_defaults()
else:
    try:
        settings = Settings.load()
    except Exception as e:
        log.exception(e)
        log.error(f'Unable to load settings error: {e} , regenerating...')
        settings = Settings.restore_defaults()

log.setLevel(settings.log_level)

if not ISSUES_LIST.exists():
    log.info(f'Issues list: "{ISSUES_LIST}" not found, creating new list')
    with open(ISSUES_LIST, 'w') as f:
        f.write('[]')

if not DELETED_ISSUES_LIST.exists():
    log.info(
        f'Deleted Issues list: "{DELETED_ISSUES_LIST}" not found, creating new list')
    with open(DELETED_ISSUES_LIST, 'w') as f:
        f.write('[]')

factory = Factory(settings)

try:
    log.info("Initializing Launcher")
    launcher: ILauncherService = factory.get_launcher_service()
    log.info("Starting application")
    launcher.run_main_window()
except Exception as ex:
    log.exception(ex)
