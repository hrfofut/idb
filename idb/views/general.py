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
    req = requests.get('https://api.github.com/repos/hrfofut/idb/stats/contributors')
    req_list = req.json()
    commit_count = {'total': 0}
    for contributor in req_list:
        commit_count[contributor['author']['login']] = contributor['total']
        commit_count['total'] += contributor['total']
    req_issue = requests.get('https://api.github.com/repos/hrfofut/idb/issues?state=all&page=1&per_page=500')
    for issue in (req_issue.json()):
        iss_total += 1
        iss_count[logins[issue['user']['login']]] += 1
    iss_count.append(iss_total)
    return render_template('about.html', commits=commit_count, issues=iss_count)

# Error handling
