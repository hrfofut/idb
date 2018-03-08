from flask import Blueprint, render_template, abort

import requests
import json

general = Blueprint('general', __name__)


@general.route("/")
def splash(name=None):
    return render_template('index.html')


@general.route("/about")
def about():
    logins = {'cindyqtruong': 0, 'BrandonHarrisonCode': 1, 'hrfofut': 2, 'straitlaced': 3, 'fantomats15': 4}
    iss_count = []
    iss_total = 0
    for i in range(0, 5):
        iss_count.append(0)
    req_issue = requests.get('https://api.github.com/repos/hrfofut/idb/issues?state=all&page=1&per_page=500')
    for issue in (req_issue.json()):
        iss_total += 1
        iss_count[logins[issue['user']['login']]] += 1
    iss_count.append(iss_total)

    # get commits
    commit_count = {'total': 0, 'cindyqtruong': 0, 'BrandonHarrisonCode': 0, 'hrfofut': 0, 'straitlaced': 0, 'fantomats15': 0}
    req_commit = requests.get('https://api.github.com/repos/hrfofut/idb/stats/contributors')
    if req_commit.status_code == requests.codes.ok:
        req_commit_json = req_commit.json()
        if isinstance(req_commit_json, list):
            for cont in req_commit_json:
                commit_count[cont['author']['login']] = cont['total']
                commit_count['total'] += cont['total']

    # get issues

    return render_template('about.html', commits=commit_count, issues=iss_count)

# Error handling
