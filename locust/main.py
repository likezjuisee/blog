#coding=gbk
from locust import HttpLocust, TaskSet, task
import random, string, json

def genRandomMid():
    a = list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:32])

def genMids(midNum=1000):
    mids = []
    for i in range(midNum):
        mids.append(genRandomMid())
    return mids

class UserBehavior(TaskSet):

    mid = ''

    @task
    def nginx(self):
        response = self.client.get('/', catch_response=True)
        if response.status_code == 200:
            response.success()

    def heartBeat(self):
        headers = {
                      r'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
                      'Cache-Control': 'no-cache'
                  }
        response = self.client.post('/api/heartbeat.json?mid=%s&md5=961bc340de811cfce938625796304236' % self.mid, data='', headers=headers, catch_response=True)
        if response.status_code == 200:
            response.success()

    def updateClientInfo(self):
        headers = {
                      r'Content-Type': 'application/x-www-form-urlencoded',
                  }
        data = {"key":"","os":100729089,"report_ip":"10.18.131.59","group":"WORKGROUP","user_name":"perftest",\
                "osex":0,"computer_name":"perftest-PC","mac":"8851fb469a97","ie_ver":"11.0.9600.16428","sys_space":81511}
        data = json.dumps(data)
        response = self.client.post('/api/update_client_info.json?mid=%s&ver=1.0' % self.mid, data=data, headers=headers, catch_response=True)
        if response.status_code == 200:
            response.success()

    def getTask(self):
        headers = {
                      r'Content-Type': 'application/x-www-form-urlencoded',
                  }
        data = {"ws":["base_seaccatting","popwnd_setting","startup_assistant","safe_protect","leak_repair","xp_fix"]}
        data = json.dumps(data)
        response = self.client.post('/api/getconf.json?mid=%s&ver=1.0' % self.mid, data=data, headers=headers, catch_response=True)
        if response.status_code == 200:
            response.success()

    def opentest(self):
        headers = {
                      'Cookie':'LSesson=12b8e82c9c2546318bd9e77217058c29',
                  }
        response = self.client.get(r'/arcus/device/getPrivateDeviceList', headers=headers, catch_response=True)
        if response.status_code == 200:
            response.success()

    def opentestAttributeList(self):
        headers = {
                      'Cookie':'LSesson=12b8e82c9c2546318bd9e77217058c29',
                  }
        response = self.client.get(r'/arcus/jiagu/getPrivateAttributeList', headers=headers, catch_response=True)
        if response.status_code == 200:
            response.success()

    def opentestNginx(self):
        headers = {
                   'Connection':'keep-alive',
                   'Cache-Control':'no-cache',
                  }
        response = self.client.get(r'/test121212.html', headers=headers, catch_response=True)
        if response.status_code == 200:
            response.success()

    def on_start(self):
        pass

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=1
    max_wait=1