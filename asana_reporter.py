import json
import requests
import time
from calendar import timegm

user_info=json.load(open('user_info.json', 'r'))
asana_api_key = user_info['asana_api_key']
asana_url = 'https://app.asana.com/api/1.0/'
tag_id = user_info['tag_id'] 
tag_url = 'tags/'  + tag_id + '/tasks'
beeminder_username= user_info['beeminder_username'] 
goal_name = user_info['goal_name'] 
beeminder_auth_token= user_info['beeminder_auth_token'] 
beeminder_url = 'https://www.beeminder.com/api/v1/users/' + beeminder_username + '/goals/' + goal_name
current_time=time.time()

# Get ids of tagged tasks
asana_request=requests.get(asana_url + tag_url, auth=(asana_api_key,'')).json()

# Get tagged tasks
tasks=[requests.get(asana_url + 'tasks/' + str(t['id']), auth=(asana_api_key,'')).json() for t in asana_request['data']]

# In tagged tasks, untag completed ones
for t in tasks:
    if t['data']['completed']:
        r=requests.post(asana_url + 'tasks/' + str(t['data']['id']) + '/removeTag', data={'tag':tag_id}, auth=(asana_api_key, ''))

# Construct datapoints from completed tasks
beeminder_payload={'datapoints':json.dumps([{"timestamp": iso_to_epoch(t['data']['completed_at']), "value":1, "comment":t['data']['name']} for t in tasks if t['data']['completed']]), 'auth_token': beeminder_auth_token}

r=requests.post(beeminder_url + '/datapoints/create_all.json', data=beeminder_payload)

def iso_to_epoch(iso_time):
    time_obj=time.strptime(iso_time[:-5],'%Y-%m-%dT%H:%M:%S')
    return timegm(time_obj)

