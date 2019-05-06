import time
import base64
import requests
import json

BASE_URL = 'http://cmp.xspinfo.com:90/jsonServer.php'

class SPUser():

    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd



    '''登录服务器'''
    def loginserver(self):
        stamp = self.gettimestamp()

        jsondic = {'clientVersion': '2.0',
                   'souse': 'Eomp',
                   'user': self.name,
                   'pwd': self.pwd}

        parmrs = {'action': 'Login',
                  'cid': '6',
                  'jsonstr': json.dumps(jsondic),
                  'stamp': stamp,
                  }

        response = requests.get(BASE_URL, parmrs)
        return response.json()['content']['sessionid']

    '''获取用户详情'''
    def getUserInfo(self, user_id, session_id):

        stamp = self.gettimestamp()

        jsondic = {'clientVersion': '2.0',
                   'Enum': user_id}

        parmrs = {'action': 'contactDetail',
                  'cid': '6',
                  'jsonstr': json.dumps(jsondic),
                  'stamp': stamp,
                  'sessionid': session_id
                  }
        response = requests.post(BASE_URL, parmrs)
        if 'content' in response.json():
            return response.json()['content']
        else:
            return ''

    '''获取用户详情'''
    def getAllAddressInfo(self, session_id):
        stamp = self.gettimestamp()
        jsondic = {'clientVersion': '2.0',
                   'keywords': '',
                   'type': '1',
                   'page': '0'}
        parmrs = {'action': 'addrbookList',
                  'cid': '6',
                  'jsonstr': json.dumps(jsondic),
                  'stamp': stamp,
                  'sessionid': session_id
                  }
        response = requests.get(BASE_URL, parmrs)
        datas = response.json()['content']
        return datas

    '''获取时间戳'''
    def gettimestamp(self):
        timestamp = str(time.time())
        timestamp_sc = timestamp + "_SPCMP"
        stamp = base64.b64encode(timestamp_sc.encode('utf-8'))
        return stamp



