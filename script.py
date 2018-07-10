import requests
import json

r = requests.get('http://codeforces.com/api/contest.list')
contests = filter(lambda x: x['phase'] == 'FINISHED', r.json()['result'])
top, antitop = [], []

for contest in contests:
    print(contest['name'])
    r = requests.get(
        'http://codeforces.com/api/contest.ratingChanges?contestId={}'.format(contest['id'])
    )
    
    if r.json()['status'] == 'FAILED':
        continue
        
    changes = r.json()
    if 'result' in changes:
        changes = r.json()['result']

    for c in changes:
        top.append({'oldRating': c['oldRating'],
                    'newRating': c['newRating'],
                    'handle': c['handle'],
                    'contestName': c['contestName'],
                    'ratingChange': c['newRating'] - c['oldRating'],
                    'id': contest['id']})
        antitop.append(top[-1])
        
    top.sort(reverse=True, key=lambda x: x['ratingChange'])
    antitop.sort(reverse=False, key=lambda x: x['ratingChange'])
    
    top, antitop = top[:15], antitop[:15]


print('TOP')
for idx, v in enumerate(top):
    print('<tr><th>{}</th><th>[user:{}]</th><th>+{}</th><th>[contest:{}]</th></tr>'.format(
        idx+1, v['handle'], v['ratingChange'], v['id']))

print('BOTTOM')
for idx, v in enumerate(top):
    print('<tr><th>{}</th><th>[user:{}]</th><th>-{}</th><th>[contest:{}]</th></tr>'.format(
        idx + 1, v['handle'], v['ratingChange'], v['id']))
