# my-assistant - A time tracking application built in Python 3.10

## Overview

This is a basic PySimpleGUI application built to help automate tracking work logs for the work day.

## Features

- Integrates with JIRA directly to log time to Jira issues
- Automatically prompts every hour to log time
- A backup file with automatically be stored with all your time entries if the integration fails

## 3rd Party Libraries

- [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/) for building the entire GUI
- [requests](https://docs.python-requests.org/en/latest/) for sending requests to Jira
- [Rich](https://github.com/Textualize/rich) for console output during development

## Future Updates

- Make work days of the week configurable
- Update logic to work for 3rd shift, i.e. a work day that crosses midnight
- Other integrations?
