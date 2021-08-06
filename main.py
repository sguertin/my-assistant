import logging
import logging.config

logging.basicConfig(
    level=logging.CRITICAL,
    format='%(name)-15s %(message)s',
    datefmt='[%Y-%m-%d %H:%M:%S]',
)
log = logging.getLogger('my-assistant.main')

from assistant import Assistant


my_assistant = Assistant()

my_assistant.run()
