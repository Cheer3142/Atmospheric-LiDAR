import requests
import json
import pandas as pd
from datetime import timedelta, datetime

time_slot = ['2024-03-01',
             '2024-03-07',
             '2024-02-12',
             '2024-03-11',
             '2024-03-15']

time_slot = [datetime.strptime(i, "%Y-%m-%d") for i in time_slot]
time_slot.sort()

for start_time in time_slot:    
    start       = start_time.strftime("%Y-%m-%d")
    end         = (start_time + timedelta(days = 1)).strftime("%Y-%m-%d") + 'T07:00'    
    payload     = 'station=astropark&start={}&end={}'.format(start + 'T18:00', end)

    url = ["http://192.168.2.112:3000/api/GetTempOut",
       "http://192.168.2.112:3000/api/GetWindSpeed",
       "http://192.168.2.112:3000/api/GetHumid",
       "http://192.168.2.112:3000/api/GetDewPoint",
       "http://192.168.2.112:3000/api/GetBarometer",]
    url = iter(url)

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    for Condition in range(0, 5, 1):
        response = requests.request("POST", next(url), headers=headers, data=payload)
        res = json.loads(response.text)
        if Condition:
            df[list(res[0].keys())[-1]] = [i[list(i)[-1]] for i in res]
        else:
            df = pd.DataFrame(res)
            if df.empty: exit()
            
    df['date'] = pd.to_datetime(df['date'].str[:-5],
                                format='%Y-%m-%dT%H:%M:%S')
    df['date'] = df['date'] + timedelta(hours = 7)

print(df.head())














































































