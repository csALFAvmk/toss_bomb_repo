'''
Created on 21. 7. 2017

@author: dmarkov004
'''

import json
import copy
import urllib
import requests
from urllib.request import urlopen

API = 'https://api.telegram.org/bot'
TOKEN = '441239707:AAEhqAqH_-HYWTeECmXGKGvjcgxvY2p0ogI'
#my_chat_id = '289795148'
URL = API + TOKEN
INVALID_UPDATE_ID = 0

global last_update_id
last_update_id = INVALID_UPDATE_ID


def getUpdates():
    get = URL + '/getUpdates'
    response = urlopen(get)
    return response.read()

def get_updates(self, offset=None, timeout=30):
    method = 'getUpdates'
    params = {'timeout': timeout, 'offset': offset}
    resp = requests.get(URL + method, params)
    #result_json = resp.json()['result']
    return "result_json"


def getFirstName():
    js = json.loads(getUpdates())
    update_obj = js['result'][-1]
    return update_obj['message']['from']['first_name']

def getUserName():
    js = json.loads(getUpdates())
    update_obj = js['result'][-1]
    return update_obj['message']['from']['username']

def getChatId():
    js = json.loads(getUpdates())
    update_obj = js['result'][-1]
    return update_obj['message']['chat']['id']

def getCurrentOffset():
    js=json.loads(getUpdates())
    update_obj=js['result'][-1]
    return update_obj['update_id']

def setOffset(offset):
    get = URL + '/getUpdates?offest=' + offset
    response = urlopen(get)
    return response.read()

def getBotUserList():
    js = json.loads(getUpdates())
    user=['','','','']
    UserList=[]
        
    for update_obj in js['result']:
        user[0]=copy.deepcopy(update_obj['message']['from']['first_name'])
        if 'last_name' in update_obj['message']['from']:
            user[1]=copy.deepcopy(update_obj['message']['from']['last_name'])
        else:
            user[1]=""
        if 'username' in update_obj['message']['from']:
            user[2]=copy.deepcopy(update_obj['message']['from']['username'])
        else:
            user[2]=""
        user[3]=copy.deepcopy(update_obj['message']['chat']['id'])
        
        if not UserList:
            UserList.append(copy.deepcopy(user))
        
        add_to_list=True
        for addedUser in UserList:
            if  update_obj['message']['chat']['id'] == addedUser[3]:
                add_to_list=False
        if add_to_list:
            UserList.append(copy.deepcopy(user))
    return UserList


def getCommand():
    js = json.loads(getUpdates())
    update_obj = js['result'][-1]
    
    global last_update_id
    if last_update_id == INVALID_UPDATE_ID:
        last_update_id = update_obj['update_id']
        return None

    if update_obj['update_id'] != last_update_id:
        last_update_id = update_obj['update_id']
        if 'text' in update_obj['message']:
            temp_text = update_obj['message']['text']
            if temp_text[0]=='/':
                return temp_text[1:]
            else:
                return 'dummy'
    return None

def sendMessage(chat_id, text):
    sendMessage = {
        'chat_id': chat_id,
        'text': text
    }
    get = URL + '/sendMessage?' + urllib.parse.urlencode(sendMessage)
    response = urlopen(get)
