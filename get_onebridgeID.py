# encoding:utf-8
'''
Created on 2016��7��28��

@author: Edmon
'''
from pymongo import MongoClient
import requests,json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def insertData(data):
    client  = MongoClient()
    db = client['atlas']
    coll = db['onebridge']
    coll.insert_one(data)
    client.close()

def getInfo(userid):

    headers = {'Host': 'atlascopco.1bridge.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': 1,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://atlascopco.1bridge.com/'
    }
    url = "https://atlascopco.1bridge.com/guestConference.sf"

    r = requests.post(url,data=json.dumps({"id":userid,"passcode":""}), headers=headers,verify=False)
    userinfo = r.json()
    print userinfo
    if userinfo.get('name'):
        insertData(userinfo)
        print "%s  ---  %s" %(userinfo.get('conferenceId'), userinfo.get('name'))

    
if __name__ == "__main__":
    getInfo('86700001')