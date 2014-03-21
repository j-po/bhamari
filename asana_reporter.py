import sys
import json
import requests
from calendar import timegm
import time

ASANA_URL = 'https://app.asana.com/api/1.0/'

def main(info_file='user_info.json'):
    with open(info_file, 'r') as f:
        user_info=json.load(f)
    asana_api_key = user_info['asana_api_key']
    tag_id = user_info['tag_id'] 
    beeminder_username= user_info['beeminder_username'] 
    goal_name = user_info['goal_name'] 
    beeminder_auth_token= user_info['beeminder_auth_token'] 

    asana_tasks=get_asana_tasks(asana_api_key, tag_id)

    if asana_tasks:
        beeminder_success = post_to_beeminder(beeminder_username, goal_name,
                                            beeminder_auth_token, asana_tasks)
        if beeminder_success:
            unmark_completed_tasks(asana_api_key, tag_id, asana_tasks)

def iso_to_epoch(iso_time):
    time_obj=time.strptime(iso_time[:-5],'%Y-%m-%dT%H:%M:%S')
    # [:-5] slices off decimal places in seconds and timezone, because
    # strptime() doesn't parse them correctly
    return timegm(time_obj)

def get_asana_tasks(api_key, tag_id):
    print 'Fetching completed tasks:'
    asana_request=requests.get(ASANA_URL + 'tags/' + tag_id + '/tasks',
                                auth=(api_key,'')).json()

    #TODO: Would this be nicer if it were asynchronous? Probably yes.
    tasks=[requests.get(ASANA_URL + 'tasks/' + str(t['id']),
                        auth=(api_key,'')).json()
            for t in asana_request['data']]
    completed_tasks = [t for t in tasks if t['data']['completed']]
    print completed_tasks
    return completed_tasks

def post_to_beeminder(username, goal, auth_token, tasks):
    print 'Posting task completions to Beeminder:'
    beeminder_payload={
        "auth_token": auth_token,
        'datapoints':json.dumps([{
            "timestamp": iso_to_epoch(t['data']['completed_at']),
            "value":1, 
            "comment":t['data']['name']}
        for t in tasks])}
    beeminder_url = ('https://www.beeminder.com/api/v1/users/' +
                            username + '/goals/' + goal +
                            '/datapoints/create_all.json')
    print beeminder_payload
    r=requests.post(beeminder_url, params=beeminder_payload)
    print r.text
    if r.status_code==requests.codes.ok:
        return True
    else:
        print 'Beeminder request failed'
        return False

def unmark_completed_tasks(api_key, tag_id, tasks):
    for t in tasks:
        if t['data']['completed']:
            r=requests.post(ASANA_URL + 'tasks/' + str(t['data']['id'])
                            + '/removeTag',
                            data={'tag':tag_id}, auth=(api_key, ''))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
