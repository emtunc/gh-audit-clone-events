import os
import time
from datetime import datetime

import requests

GITHUB_ORG = os.environ.get("GITHUB_ORG")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

headers = {'Accept': 'application/vnd.github.v3+json',
           f'Authorization': 'token ' + GITHUB_TOKEN,
           'User-Agent': 'github.com/emtunc/gh-audit-clone-events'}


def remaining_rate_limit():
    rate_limit = requests.get(f"https://api.github.com/rate_limit", headers=headers).json()
    # print(f"Remaining rate limit: {rate_limit['rate']['remaining']}")
    return rate_limit['rate']['remaining']


def clone_events():
    while remaining_rate_limit() > 0:
        git_audit_events = requests.get(f"https://api.github.com/orgs/{GITHUB_ORG}/audit-log?include=git&per_page=50",
                                        headers=headers)
        git_audit_events_json = git_audit_events.json()
        if git_audit_events.status_code == 200:
            for event in git_audit_events_json:
                if event['action'] == 'git.clone' and event['repository_public'] is False:
                    timestamp = datetime.fromtimestamp(event['@timestamp'] / 1000).strftime("%Y-%m-%d %I:%M:%S")
                    print(f"Timestamp: {timestamp}\n"
                          f"Action: {event['action']}\n"
                          f"Repo: {event['repository']}\n"
                          f"Actor: {event['actor']}\n"
                          f"Transport protocol: {event['transport_protocol_name']}\n")
        elif git_audit_events.status_code == 502:
            print(f"Got back a server error. It's a BETA API so it should fix itself after a few tries...")
        else:
            print(f"ERROR: {git_audit_events.content}")
        time.sleep(5)


clone_events()
