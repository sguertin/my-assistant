import base64

from ui.credentials import credentials_prompt

def get_auth():
    user_name, password = credentials_prompt()
    encoding = base64.b64encode(f'{user_name}:{password}'.encode('utf-8'))    
    return encoding.decode()