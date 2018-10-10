import requests
from urllib.parse import urlencode
import time
import json

Token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

id = 'eshmargunov'


def found_groups(id, Token):

    if type(id) is not int:
    
        params = {
                  'screen_name': id,
                  'access_token': Token,
                  'v': '5.74'
                 }

        response = requests.get('https://api.vk.com/method/utils.resolveScreenName',params)
        id = response.json()['response']['object_id']

    params = {
              'user_id': id,
              'access_token': Token,
              'v': '5.74'
            }

    response = requests.get('https://api.vk.com/method/friends.get',params)
    freinds_id = response.json()['response']['items']

    response = requests.get('https://api.vk.com/method/groups.get',params)
    groups_id = response.json()['response']['items']

    groups_alone_id = []
    count = 0

    for group in groups_id:
    
        params = {
                  'access_token': Token,
                  'v': '5.74',
                  'group_id': group 
                 }

        response = requests.get('https://api.vk.com/method/groups.getMembers',params)
    
        count += 1
        print(count, '/', len(groups_id))
    
        if 'response' in response.json():

            group_members = response.json()['response']['items']
            members_count = response.json()['response']['count']
    
            flag = False
    
            for friend in freinds_id:
                if friend in group_members:
                    flag = True
            
            if flag == False:
            
                response = requests.get('https://api.vk.com/method/groups.getById',params)

                group_info = {
                              'Name': response.json()['response'][0]['name'],
                              'id': response.json()['response'][0]['id'],
                              'members_count': members_count
                             }
            
                groups_alone_id.append (group_info)
        
        time.sleep(0.5)

    with open("out_put", "w", encoding="utf-8") as file:
        json.dump(groups_alone_id, file, ensure_ascii=False, indent=2)
        
    return groups_alone_id


found_groups(id, Token)

