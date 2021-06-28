import json

from config import ISSUES_LIST

def get_raw_issues() -> list[dict]:
    with open(ISSUES_LIST, 'r') as f:
        return json.loads(f.read())
    
def save_issues_list(issues_list: list[dict]):
    with open(ISSUES_LIST, 'w') as f:
        f.write(json.dumps(issues_list))

def get_issues_list() -> tuple[list[str],dict]:    
    issues_list = get_raw_issues()
    issues_map = {}
    if (len(issues_list) == 0):
        return [], {}
    for issue in issues_list:
        issue_num, description = issue['issue_num'], issue['description']
        key = f'{issue_num} - {description}'
        issues_map[key] = issue
    return list(issues_map.keys()), issues_map

def add_issue(issue: dict) -> str:
    issues_list = get_raw_issues()
    issues_list.append(issue)
    save_issues_list(issues_list)
    issue_num, description = issue['issue_num'], issue['description']
    return f'{issue_num} - {description}'