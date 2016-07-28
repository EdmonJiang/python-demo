# encoding:utf-8
'''
Created on 2016.7.28

@author: ssiej
'''
from pymongo import MongoClient
import multiprocessing
import gevent
from gevent import Greenlet
from gevent import monkey
from gevent.queue import JoinableQueue
monkey.patch_all()
import requests,json, time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class MyGreenlet(Greenlet):

    def __init__(self, q):
        Greenlet.__init__(self)
        self.q = q

    def _run(self):
        while True:
            getInfo(self.q.get())
            self.q.task_done()

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
    try:
        r = requests.post(url,data=json.dumps({"id":userid,"passcode":""}), headers=headers,verify=False)
        userinfo = r.json()
#         print userinfo
#         if userinfo.get('name'):
#             insertData(userinfo)
#             print "%s  ---  %s" %(userinfo.get('conferenceId'), userinfo.get('name'))
        insertData(userinfo)
        print "%s  ---  %s" %(userinfo.get('conferenceId'), userinfo.get('name'))

    except Exception:
        pass

def insertData(data):
    client  = MongoClient()
    db = client['atlas']
    coll = db['onebridge']
    coll.insert_one(data)
    client.close()

def createThread(nums):
    strnums = [str(x) for x in nums]
    q = JoinableQueue()
    for i in strnums:
        q.put(i)
    
    for i in range(10):
        t = MyGreenlet(q)
        t.start()
    
    q.join()
    print "It's done! "

if __name__ == '__main__':
    start = time.time()
    fnum = 86700001
    lnum = 86700301
    n = 4
    part = (lnum - fnum)/n
    numlist = map(lambda x:xrange(x*part+fnum, x!=n-1 and (x+1)*part+fnum or lnum+1),range(n))
    t = []
    for nums in numlist:
        p = multiprocessing.Process(target=createThread, args=(nums,))
        p.start()
        t.append(p)
    
    for each in t:
        each.join()
    end = time.time()
    print "It's done! -- %f s" % (end - start) 
