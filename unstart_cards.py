#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Automate unstart pivotal cards"""

import ast
from json import dumps

import requests

TOKEN = 'ef4ca633d4da0a863abcde9d5dffa6fd'
PROJECT_ID = 1575317

def get_story_infor(token=TOKEN, project_id=PROJECT_ID):
    """
    Get started story id
    """
    headers = {'X-TrackerToken': token}
    url = f"https://www.pivotaltracker.com/services/v5/projects/{project_id}/stories?date_format=millis&with_state=started"
    r = requests.get(url, headers=headers)
    infor_ls = ast.literal_eval(r.text)
    story_infor_dict = {}
    for infor in infor_ls:
        story_id = infor['id']
        story_points = 'NA'
        try:
            story_points = int(infor['estimate'])
        except:
            pass
        story_infor_dict[story_id] = story_points
    return story_infor_dict


def update_story_states(token=TOKEN, project_id=PROJECT_ID):
    """
    Change story states and points
    """
    headers = {'X-TrackerToken': token,
               'Content-Type': 'application/json'}
    story_infor = get_story_infor(token, project_id)
    for story_id, story_point in story_infor.items():
        state = {"current_state":"unstarted"}
        url = f"https://www.pivotaltracker.com/services/v5/projects/{PROJECT_ID}/stories/{story_id}"
        if story_point != 'NA':
            if story_point <= 2:
                state["estimate"] = story_point + 1
        p = requests.put(url, headers=headers, data=dumps(state))
        print(p.content)
    return p.content

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    status = update_story_states()
    print(status)

