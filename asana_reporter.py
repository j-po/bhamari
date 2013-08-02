import json
import requests
import time

asana_api_key = '' #SET THIS
asana_url = 'https://app.asana.com/api/1.0/'
tag_id = '' #SET THIS 
tag_url = 'tags/'  + tag_id + '/tasks'
beeminder_username= '' #SET THIS 
goal_name = '' #SET THIS 
beeminder_auth_token= '' #SET THIS 
beeminder_url = 'https://www.beeminder.com/api/v1/users/' + beeminder_username + '/goals/' + goal_name
current_time=time.time()

asana_request=requests.get(asana_url + tag_url, auth=(asana_api_key,'')).json()

tasks=[requests.get(asana_url + 'tasks/' + str(t['id']), auth=(asana_api_key,'')).json() for t in asana_request['data']]

for t in tasks:
    if t['data']['completed']:
        r=requests.post(asana_url + 'tasks/' + str(t['data']['id']) + '/removeTag', data={'tag':tag_id}, auth=(asana_api_key, ''))

beeminder_payload={'datapoints':json.dumps([{"timestamp":current_time, "value":1, "comment":t['data']['name']} for t in tasks if t['data']['completed']]), 'auth_token': beeminder_auth_token}

r=requests.post(beeminder_url + '/datapoints/create_all.json', data=beeminder_payload)

