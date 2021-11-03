import logging
from typing import Callable

import PySimpleGUI as sg

from my_assistant.models.settings import Settings
from my_assistant.constants import HOUR_RANGE, MINUTE_RANGE, DAYS_OF_WEEK, LOGGING_LEVELS
from my_assistant.events import SAVE_EVENT, CANCEL_EVENT, CLOSE_EVENTS


def change_settings(settings: Settings, create_new_settings: Callable[[dict, str, frozenset[int]], Settings]):
    original_settings: Settings = Settings.from_dict(settings.to_dict())
    day_checkboxes = []
    log = logging.getLogger('ui.sg.change_settings')
    log.setLevel(settings.log_level)

    for day in DAYS_OF_WEEK.keys():
        day_checkboxes.append(sg.Checkbox(
            day, key=day, default=DAYS_OF_WEEK[day] in settings.days_of_week))
    window = sg.Window(f'Settings', [
        [sg.T('Jira Url (e.g. https://jira.yourcompany.com):'),
         sg.In(settings.base_url, key='base_url')],
        [sg.T('Start Time of Day:'), sg.Combo([f'{hour:02d}' for hour in HOUR_RANGE], default_value=settings.start_hour, key='start_hour'),
         sg.T(':'), sg.Combo([f'{minute:02d}' for minute in MINUTE_RANGE], default_value=settings.start_minute, key='start_minute')],
        [sg.T('End Time of Day:'), sg.Combo([f'{hour:02d}' for hour in HOUR_RANGE], default_value=settings.end_hour, key='end_hour'),
         sg.T(':'), sg.Combo([f'{minute:02d}' for minute in MINUTE_RANGE], default_value=settings.end_minute, key='end_minute')],
        [sg.T('Time Recording Interval:'), sg.Combo([0, 1, 2, 3, 4, 5, 6, 7, 8], key='interval_hours'),
         sg.T('h '), sg.Combo(['00', '15', '30', '45'], key='interval_minutes'), sg.T('m')],
        [sg.Checkbox('Enable Jira', key='enable_jira')],
        day_checkboxes,
        [sg.Submit('Save', key=SAVE_EVENT), sg.Button(
            'Cancel', key=CANCEL_EVENT)],
    ])
    width, height = window.size
    log.debug(f'WINDOW DIMENSIONS : WIDTH={width} HEIGHT={height} ')
    while True:
        event, values = window.read()
        log.debug(f'EVENT \'{event}\' RECEIVED')
        if event == SAVE_EVENT:
            settings = create_new_settings(values, settings.theme, frozenset(
                value for day, value in DAYS_OF_WEEK.items() if values[day]))
            log.debug(f'NEW SETTINGS: {settings}')
            window.close()
            return settings
        elif event in CLOSE_EVENTS:
            log.debug(f'SETTINGS REVERTED: {original_settings}')
            window.close()
            return original_settings

        window.refresh()
