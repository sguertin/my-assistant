from datetime import datetime
import logging
import logging.config
from os import getenv, mkdir
from pathlib import Path
from time import sleep

import PySimpleGUIQt as sg

logging.basicConfig(
    level=logging.CRITICAL,
    format='%(name)-15s %(message)s',
    datefmt='[%Y-%m-%d %H:%M:%S]',
)
sg.theme('DarkBlue3') 

log = logging.getLogger('TimeTracking')
log.setLevel(logging.INFO)

working_dir = Path(getenv('USERPROFILE'), 'TimeTracking')
last_hour = 0
def get_task_file_path(date: datetime) -> Path:
    return Path(working_dir, f'TimeTracking-{date.year}-{date.month}-{date.day}.log') 

current_task = get_task_file_path(datetime.now())
if (current_task.exists()):
    log.info(f'Existing tracking found at {current_task}')
    with open(str(current_task)) as f:
        for line in f:
            pass
        last_line = line
    
    last_hour = int(last_line.partition('-')[2].partition(':')[0])
    log.info(f'Last hour recorded: {last_hour}:00')

        

if not working_dir.exists():
    log.info(f'Working directory not found at {working_dir}, creating...')
    mkdir(str(working_dir))
    
def create_entry(date: datetime, entry: str):    
    task_file = get_task_file_path(date)
    task_file_exists = task_file.exists()
    with open(str(task_file), 'a+') as f:
        if not task_file_exists:
            log.info(f'Starting new file: {task_file}')
            f.write(f'---------TimeTracking-{date.year}-{date.month}-{date.day}---------\n')
        f.write(f'{date.hour - 1}:00-{date.hour}:00 - {entry}\n')
    log.info(f'Entry logged for {date.hour}:00')

def is_workday(date: datetime) -> bool:
    return date.weekday() < 5

def is_workhour(date: datetime) -> bool:
    return date.hour > 8 and date.hour <= 17

now = datetime.now()
log.info('Initialization is complete, starting...')
while True:    
    if is_workday(now) and is_workhour(now) and now.hour != last_hour:
        last_hour = now.hour
        event, values = sg.Window(f'Time Tracking',
            [
                [sg.T(f'What have you been working on for {now.hour - 1}:00 - {now.hour}:00?'), sg.In(key='entry')],
                [sg.Submit('OK'), sg.Cancel('Cancel') ]
            ]
        ).read(close=True)
        entry = values['entry']
        create_entry(now, entry)
    now = datetime.now()
    sleep(300)
