from datetime import datetime
import logging
from pathlib import Path

from config import WORKING_DIR

log = logging.getLogger('TimeTracking')
log.setLevel(logging.INFO)

def create_tracking_entry(date: datetime, entry: str):    
    task_file = get_log_file_path(date)
    task_file_exists = task_file.exists()
    with open(str(task_file), 'a+') as f:
        if not task_file_exists:
            log.info(f'Starting new file: {task_file}')
            f.write(f'---------TimeTracking-{date.year}-{date.month}-{date.day}---------\n')
        f.write(f'{date.hour - 1}:00-{date.hour}:00 - {entry}\n')
    log.info(f'Entry logged for {date.hour}:00')

def get_log_file_path(date: datetime) -> Path:
    return Path(WORKING_DIR, f'TimeTracking-{date.year}-{date.month}-{date.day}.log')

def get_last_hour() -> int:
    current_task = get_log_file_path(datetime.now())
    if (current_task.exists()):
        log.info(f'Existing tracking found at {current_task}')
        with open(str(current_task)) as f:
            for line in f:
                pass
            last_line = line
        
        last_hour = int(last_line.partition('-')[2].partition(':')[0])
        log.info(f'Last hour recorded: {last_hour}:00') 
        return last_hour
    else:
        return 0
    
def create_tracking_entry(date: datetime, entry: str):    
    task_file = get_log_file_path(date)
    task_file_exists = task_file.exists()    
    with open(str(task_file), 'a+') as f:
        if not task_file_exists:
            log.info(f'Starting new file: {task_file}')
            f.write(f'---------TimeTracking-{date.year}-{date.month}-{date.day}---------\n')
        f.write(f'{date.hour - 1}:00-{date.hour}:00 - {entry}\n')
    log.info(f'Entry logged for {date.hour}:00')