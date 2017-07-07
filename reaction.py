import requests
import json
from os.path import join
from requests.auth import HTTPBasicAuth

BASE = 'https://api.github.com/repos/chaosbot/chaos/'

EMOJIS = [
        "heart", "blue_heart"
        ]

def request(url, method, useBase=True, data=None):
    _BASE = BASE if useBase else ""
    r = getattr(requests, method)(
        _BASE + url,
        headers={'Accept': 'application/vnd.github.squirrel-girl-preview'},
        json=data,
        auth = HTTPBasicAuth('e-beach', 'supersecretpw')
    )
    r.raise_for_status()
    content = json.loads(r.text)
    return content

def get(url):
    useBase = 'https://' not in url
    return request(url, 'get', useBase)

def thumbs_up(issue_no):
   return request(
        join('issues', str(issue_no), 'reactions'),
        'post',
       data = { 'content': '+1' }
   )

def hugs_all_around():
    pulls = get('pulls')
    for pull in pulls:
        href = pull['_links']['self']['href']
        print(href)
        number = href.split('/')[-1]
        thumbs_up(number)
    print('upvoted {} pull requests\n'.format(len(pulls)))

if __name__ == "__main__":
    # from https://stackoverflow.com/a/474543/5749914
    import sched, time
    s = sched.scheduler(time.time, time.sleep)
    def do_something(sc): 
        print("upvoting pull requests...")
        hugs_all_around()
        s.enter(60, 1, do_something, (sc,))
    s.enter(0, 1, do_something, (s,))
    s.run()
