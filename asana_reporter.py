import sys
import json
import requests
from calendar import timegm
import time

#from twisted.internet import reactor, task

ASANA_URL = 'https://app.asana.com/api/1.0/'

class Reporter(object):
    def __init__(self, info_file='user_info.json'):
        with open(info_file, 'r') as f:
            user_info=json.load(f)
        self.asana_api_key = user_info['asana_api_key']
        self.tag_id = user_info['tag_id'] 
        self.beeminder_username= user_info['beeminder_username'] 
        self.goal_name = user_info['goal_name'] 
        self.beeminder_auth_token= user_info['beeminder_auth_token'] 

    def main_workflow(self):
        asana_tasks = self.get_asana_tasks()
        if asana_tasks:
            beeminder_success = self.post_to_beeminder(asana_tasks)
            if beeminder_success:
                self.unmark_completed_tasks(asana_tasks)
        
    def get_asana_tasks(self):
        print 'Fetching completed tasks:'
        asana_request=requests.get(ASANA_URL + 'tags/' + self.tag_id + '/tasks',
                                    auth=(self.asana_api_key,'')).json()
        print asana_request
    
        #TODO: Would this be nicer if it were asynchronous? Probably yes.
        tasks=[requests.get(ASANA_URL + 'tasks/' + str(t['id']),
                            auth=(self.asana_api_key,'')).json()
                for t in asana_request['data']]
        completed_tasks = [t for t in tasks if t['data']['completed']]
        print completed_tasks
        return completed_tasks
    
    def post_to_beeminder(self, tasks):
        print 'Posting task completions to Beeminder:'
        beeminder_payload={
            "auth_token": self.beeminder_auth_token,
            'datapoints':json.dumps([{
                "timestamp": iso_to_epoch(t['data']['completed_at']),
                "value":1, 
                "comment":t['data']['name']}
            for t in tasks])}
        beeminder_url = ('https://www.beeminder.com/api/v1/users/' +
                                self.beeminder_username + '/goals/' + self.goal_name +
                                '/datapoints/create_all.json')
        print beeminder_payload
        r=requests.post(beeminder_url, params=beeminder_payload)
        print r.text
        if r.status_code==requests.codes.ok:
            return True
        else:
            print 'Beeminder request failed'
            return False
    
    def unmark_completed_tasks(self, tasks):
        for t in tasks:
            if t['data']['completed']:
                r=requests.post(ASANA_URL + 'tasks/' + str(t['data']['id'])
                                + '/removeTag',
                                data={'tag':self.tag_id}, auth=(self.asana_api_key, ''))
        
def iso_to_epoch(iso_time):
    time_obj=time.strptime(iso_time[:-5],'%Y-%m-%dT%H:%M:%S')
    # [:-5] slices off decimal places in seconds and timezone, because
    # strptime() doesn't parse them correctly
    return timegm(time_obj)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        r = Reporter(sys.argv[1])
    else:
        r = Reporter()
    r.main_workflow()
