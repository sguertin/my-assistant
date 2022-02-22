import logging
import logging.config
from os import mkdir

from my_assistant.providers.authentication import BasicAuthenticationProvider
from my_assistant.providers.ui import UIProvider

from my_assistant.constants import WORKING_DIR, ISSUES_LIST, DELETED_ISSUES_LIST, SETTINGS_FILE
from my_assistant.models.settings import Settings
from my_assistant.services.assistant import Assistant
from my_assistant.services.time_tracking import get_time_tracking_service
from my_assistant.ui.warning import warning_prompt, warning_retry_prompt
from my_assistant.ui.credentials import credentials_prompt
from my_assistant.ui.time_tracking import record_time
from my_assistant.ui.launcher import Launcher


logging.basicConfig(
    level=logging.CRITICAL,
    format='%(name)-15s %(message)s',
    datefmt='[%Y-%m-%d %H:%M:%S]',
)
log = logging.getLogger('Main')

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

auth_provider = BasicAuthenticationProvider()


def create_dependencies() -> 'tuple[Assistant, Settings]':
    settings = Settings.load()
    ui_provider = UIProvider(
        warning_prompt, warning_retry_prompt, record_time, credentials_prompt)
    time_tracking = get_time_tracking_service(
        auth_provider, ui_provider, settings)
    assistant = Assistant(time_tracking, ui_provider, settings)
    return assistant, settings


try:
    assistant, settings = create_dependencies()
    launcher = Launcher(assistant, settings)
    launcher.run_main_window(create_dependencies)
except Exception as e:
    log.error(e)
