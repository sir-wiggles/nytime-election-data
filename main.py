import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime

#  -H 'if-none-match: "2903f346ef4b0e03bf4fabbd92ebe472"' \
#  -H 'if-modified-since: Fri, 06 Nov 2020 22:56:13 GMT' \

states = [
    'georgia',
    'nevada',
    'pennsylvania',
    'arizona'
]


data = {}
raw = {}

for state in states:
    url = f'https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/race-page/{state}/president.json'
    results = requests.get(url)
    print(state, results)
    if results.status_code != 200:
        print(":(", results.status_code)
        continue
    body = results.json()
    raw[state] = body
    timeseries = body['data']['races'][0]['timeseries']

    df = pd.DataFrame()
    for event in timeseries:
        df = df.append({
            'vp': event['eevp'],
            'dvs': event['vote_shares']['bidenj'],
            'rvs': event['vote_shares']['trumpd'],
            'votes': event['votes'],
            'timestamp': event['timestamp']
        }, ignore_index=True)

    df.index = df['vp']
    df.drop(columns=['vp'], inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%dT%H:%M:%SZ")
    #  df.drop(columns=['timestamp'], inplace=True)
    data[state] = df


fig, axes = plt.subplots(nrows=4, ncols=1)
fig.tight_layout()

for i, (state, df) in enumerate(data.items()):
    df.sort_index(inplace=True)
    df[(df.index >= 90)][['dvs', 'rvs']].plot(title=state, ax=axes[i], xlabel="")
plt.show()


