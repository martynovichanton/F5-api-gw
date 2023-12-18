
import flask
import requests
import json

import urllib3
import pandas as pd
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from . Crypto import Crypto
import getpass
import gc

class F5:
    def __init__(self, device_ip, token):
        self.crypto = Crypto()
        self.device_ip = device_ip
        self.url = "https://" + self.device_ip
        self.payload = ""
        self.headers = self.crypto.encrypt_random_key(json.dumps({
            'Content-Type': "application/json",
            'X-F5-Auth-Token': token,
            'cache-control': "no-cache"
        }))

    def get_pool_names(self):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool"
        pool_names = []
        pools = requests.get(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify=False)     
        if pools.status_code is not 200:
            return "Error"
        else:
            for pool in pools.json()['items']:
                tildPath = pool['fullPath'].replace('/','~')
                pool_names.append(tildPath)
            return {"pool_names":pool_names}        

    def get_pool_config(self, pool_name):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool/" + pool_name
        pool = requests.get(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify=False)
        if pool.status_code is not 200:
            return "Error"
        return pool.json()

    def get_pool_members(self, pool_name):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool/" + pool_name + "/members"
        pool_members = requests.get(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify=False)
        if pool_members.status_code is not 200:
            return "Error"
        return pool_members.json()

    def get_pool_members_filtered(self, pool_name):
        pool_members = self.get_pool_members(pool_name)
        if "Error" in pool_members:
            return "Error"
        pool_members_filtered = []
        pool_dict = {}
        for item in pool_members['items']:
            pool_dict.update({'name':item['name']})
            pool_dict.update({'address':item['address']})
            pool_dict.update({'priorityGroup':item['priorityGroup']})
            pool_dict.update({'state':item['state']})
            pool_members_filtered.append(pool_dict)
            pool_dict = {}
        return {"pool_members":pool_members_filtered}

    def get_pool_members_stats(self, pool_name):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool/" + pool_name + "/members/stats"
        pool_members_stats = requests.get(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify=False)
        if pool_members_stats.status_code is not 200:
            return "Error"
        return pool_members_stats.json()

    def get_pool_members_stats_filtered(self, pool_name):
        pool_members_stats = self.get_pool_members_stats(pool_name)
        if "Error" in pool_members_stats:
            return "Error"
        pool_members_stats_filtered = []
        member_dict = {}

        i = 0
        for ps in pool_members_stats['entries']:
            member_dict.update({'pool_name':pool_members_stats['entries'][ps]['nestedStats']['entries']['poolName']['description']})
            member_dict.update({'name':pool_members_stats['entries'][ps]['nestedStats']['entries']['nodeName']['description']})
            member_dict.update({'address':pool_members_stats['entries'][ps]['nestedStats']['entries']['addr']['description']})
            member_dict.update({'connections':pool_members_stats['entries'][ps]['nestedStats']['entries']['serverside.curConns']['value']})
            pool_members_stats_filtered.append(member_dict)
            member_dict = {}
            i = i + 1

        return {"pool_members":pool_members_stats_filtered}

    def get_pool_members_stats_filtered_table(self, pool_name):
        pool_members_stats_filtered = self.get_pool_members_stats_filtered(pool_name)
        if "Error" in pool_members_stats_filtered:
            return "Error"
        pool_members_stats_filtered_table = pd.DataFrame(pool_members_stats_filtered['pool_members']).reindex(columns=['pool_name','name','address','connections'])
        return pool_members_stats_filtered_table.to_string()

    def get_pool_members_stats_all(self):
        dataset = []
        pool_names_all = self.get_pool_names()
        if "Error" in pool_names_all:
            return "Error"
        for pool in pool_names_all['pool_names']:
            dataset.append(self.get_pool_members_stats(pool))
            time.sleep(1)
        return {"pools":dataset}
    
    def get_pool_members_stats_all_filtered(self):
        dataset = []
        pool_names_all = self.get_pool_names()
        if "Error" in pool_names_all:
            return "Error"
        for pool in pool_names_all['pool_names']:
            dataset.append(self.get_pool_members_stats_filtered(pool))
            time.sleep(1)
        return {"pools":dataset}
    
    def get_pool_members_stats_all_filtered_table(self):
        dataset = []
        pool_names_all = self.get_pool_names()
        for pool in pool_names_all['pool_names']:
            dataset.append(self.get_pool_members_stats_filtered_table(pool))
            time.sleep(1)
        return '\n'.join(dataset)
    
    def get_token(self, user, password):
        self.url = "https://" + self.device_ip + "/mgmt/shared/authn/login"
        self.payload = self.crypto.encrypt_random_key("{\n    \"username\":" + user + ",\n    \"password\":" + password + ",\n    \"loginProviderName\": \"tmos\"\n}")
        self.headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            }
        response = requests.request("POST", self.url, data=self.crypto.decrypt_random_key(self.payload), headers=self.headers, verify=False)
        #print(response.text)
        if response.status_code is not 200:
            return "Error"
        token = self.crypto.encrypt_random_key(response.json()['token']['token'])
        del response
        gc.collect()


        self.url = "https://" + self.device_ip + "/mgmt/shared/authz/tokens"
        self.payload = ""
        self.headers = self.crypto.encrypt_random_key(json.dumps({
            'X-F5-Auth-Token': self.crypto.decrypt_random_key(token),
            'cache-control': "no-cache"
        }))
        response = requests.request("GET", self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify=False)
        #print(response.text)
        if response.status_code is not 200:
            return "Error"
        del response
        gc.collect()


        self.url = "https://" + self.device_ip + "/mgmt/shared/authz/tokens/" + self.crypto.decrypt_random_key(token)
        self.payload = "{\n    \"timeout\":\"3600\"\n}"
        self.headers = self.crypto.encrypt_random_key(json.dumps({
            'Content-Type': "application/json",
            'X-F5-Auth-Token': self.crypto.decrypt_random_key(token),
            'cache-control': "no-cache"
        }))
        response = requests.request("PATCH", self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify=False)
        if response.status_code is not 200:
            return "Error"
        token = self.crypto.encrypt_random_key(response.json()['token'])  
        del response
        gc.collect()
        return self.crypto.decrypt_random_key(token)


        
    def disable_member(self, pool_name, member_name):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool/" + pool_name + "/members/" + member_name
        self.payload = "{\n\"session\":\"user-disabled\"\n}"
        response = requests.patch(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify=False)
        if response.status_code is not 200:
            return "Error"
        return response.json()
        
    def enable_member(self, pool_name, member_name):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool/" + pool_name + "/members/" + member_name
        self.payload = "{\n\"session\":\"user-enabled\"\n}"
        response = requests.patch(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify=False)
        if response.status_code is not 200:
            return "Error"
        return response.json()

    def change_member_priority(self, pool_name, member_name, priority):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool/" + pool_name + "/members/" + member_name
        self.payload = "{\n\"priorityGroup\":" + priority + "\n}"
        response = requests.patch(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify=False)
        if response.status_code is not 200:
            return "Error"
        return response.json()
        



# token = getpass.getpass('token ')

# # # # # p1 = F5("x.x.x.x", "")
# # # # # token = p1.get_token("admin", "XXXXX")

# p = F5("10.0.0.14", token)
# print(p.get_pool_names())
# print(p.get_pool_config("~Common~walla"))
# print(p.get_pool_members_filtered("~Common~walla"))
# print(p.get_pool_members_stats("~Common~walla"))
# print(p.get_pool_members_stats_filtered("~Common~walla"))
# print(p.get_pool_members_stats_filtered_table("~Common~walla"))
# p = F5("10.0.0.14", token)
# print(p.get_pool_members_stats_all_filtered_table())
# print(p.disable_member("~Common~walla", "~Common~walla.co.il:443"))
# print(p.enable_member("~Common~walla", "~Common~walla.co.il:443"))
# print(p.change_member_priority("~Common~walla", "~Common~walla.co.il:443", "0"))
