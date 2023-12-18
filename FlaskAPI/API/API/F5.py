
import flask
import requests
import json
import pandas as pd
import time
from Crypto import Crypto
import getpass
import gc
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

    ####################################################################################################
    ### POOLs
    ####################################################################################################

    def pool_names(self):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool"
        pool_names = []
        pools = requests.get(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)     
        if pools.status_code is not 200:
            return {"Error":pools.text}
        else:
            for pool in pools.json()['items']:
                tildPath = pool['fullPath'].replace('/','~')
                pool_names.append(tildPath)
            return {"pool_names":pool_names}        

    def pool_config(self, pool_name):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool/" + pool_name
        pool = requests.get(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        if pool.status_code is not 200:
            return {"Error":pool.text}
        return {"pool":pool.json()}

    def pool_members(self, pool_name):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool/" + pool_name + "/members"
        pool_members = requests.get(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        if pool_members.status_code is not 200:
            return {"Error":pool_members.text}
        return {"pool_members":pool_members.json()}

    def pool_members_filtered(self, pool_name):
        pool_members = self.pool_members(pool_name)
        if "Error" in pool_members:
            return pool_members
        pool_members_filtered = []
        pool_dict = {}
        for item in pool_members['pool_members']['items']:
            pool_dict.update({'name':item['name']})
            pool_dict.update({'address':item['address']})
            pool_dict.update({'priorityGroup':item['priorityGroup']})
            pool_dict.update({'state':item['state']})
            pool_members_filtered.append(pool_dict)
            pool_dict = {}
        return {"pool_members":pool_members_filtered}

    def pool_members_stats(self, pool_name):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool/" + pool_name + "/members/stats"
        pool_members_stats = requests.get(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        if pool_members_stats.status_code is not 200:
            return {"Error":pool_members_stats.text}
        return {"pool_members":pool_members_stats.json()}

    def pool_members_stats_filtered(self, pool_name):
        pool_members_stats = self.pool_members_stats(pool_name)
        if "Error" in pool_members_stats:
            return pool_members_stats
        pool_members_stats_filtered = []
        member_dict = {}

        i = 0
        for ps in pool_members_stats['pool_members']['entries']:
            member_dict.update({'pool_name':pool_members_stats['pool_members']['entries'][ps]['nestedStats']['entries']['poolName']['description']})
            member_dict.update({'name':pool_members_stats['pool_members']['entries'][ps]['nestedStats']['entries']['nodeName']['description']})
            member_dict.update({'address':pool_members_stats['pool_members']['entries'][ps]['nestedStats']['entries']['addr']['description']})
            member_dict.update({'connections':pool_members_stats['pool_members']['entries'][ps]['nestedStats']['entries']['serverside.curConns']['value']})
            pool_members_stats_filtered.append(member_dict)
            member_dict = {}
            i = i + 1

        return {"pool_members":pool_members_stats_filtered}

    def pool_members_stats_filtered_table(self, pool_name):
        pool_members_stats_filtered = self.pool_members_stats_filtered(pool_name)
        if "Error" in pool_members_stats_filtered:
            return pool_members_stats_filtered
        pool_members_stats_filtered_table = pd.DataFrame(pool_members_stats_filtered['pool_members']).reindex(columns=['pool_name','name','address','connections'])
        return pool_members_stats_filtered_table.to_string()

    def pool_members_stats_all(self):
        dataset = []
        pool_names_all = self.pool_names()
        if "Error" in pool_names_all:
            return pool_names_all
        for pool in pool_names_all['pool_names']:
            dataset.append(self.pool_members_stats(pool))
            time.sleep(1)
        return {"pools":dataset}
    
    def pool_members_stats_all_filtered(self):
        dataset = []
        pool_names_all = self.pool_names()
        if "Error" in pool_names_all:
            return pool_names_all
        for pool in pool_names_all['pool_names']:
            dataset.append(self.pool_members_stats_filtered(pool))
            time.sleep(1)
        return {"pools":dataset}
    
    def pool_members_stats_all_filtered_table(self):
        dataset = []
        pool_names_all = self.pool_names()
        for pool in pool_names_all['pool_names']:
            dataset.append(self.pool_members_stats_filtered_table(pool))
            time.sleep(1)
        return '\n'.join(dataset)
    
    def token(self, user, password):
        self.url = "https://" + self.device_ip + "/mgmt/shared/authn/login"
        self.payload = self.crypto.encrypt_random_key("{\n    \"username\":" + user + ",\n    \"password\":" + password + ",\n    \"loginProviderName\": \"tmos\"\n}")
        self.headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            }
        response = requests.request("POST", self.url, data=self.crypto.decrypt_random_key(self.payload), headers=self.headers, verify = False)
        if response.status_code is not 200:
            return {"Error":response.text}
        token = self.crypto.encrypt_random_key(response.json()['token']['token'])
        del response
        gc.collect()


        self.url = "https://" + self.device_ip + "/mgmt/shared/authz/tokens"
        self.payload = ""
        self.headers = self.crypto.encrypt_random_key(json.dumps({
            'X-F5-Auth-Token': self.crypto.decrypt_random_key(token),
            'cache-control': "no-cache"
        }))
        response = requests.request("GET", self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        if response.status_code is not 200:
            return {"Error":response.text}
        del response
        gc.collect()


        self.url = "https://" + self.device_ip + "/mgmt/shared/authz/tokens/" + self.crypto.decrypt_random_key(token)
        self.payload = "{\n    \"timeout\":\"3600\"\n}"
        self.headers = self.crypto.encrypt_random_key(json.dumps({
            'Content-Type': "application/json",
            'X-F5-Auth-Token': self.crypto.decrypt_random_key(token),
            'cache-control': "no-cache"
        }))
        response = requests.request("PATCH", self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        if response.status_code is not 200:
            return {"Error":response.text}
        token = self.crypto.encrypt_random_key(response.json()['token'])  
        timeout = response.json()['timeout']
        del response
        gc.collect()
        return {"token":self.crypto.decrypt_random_key(token), "timeout":timeout}


        
    def disable_member(self, pool_name, member_name):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool/" + pool_name + "/members/" + member_name
        self.payload = "{\n\"session\":\"user-disabled\"\n}"
        response = requests.patch(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        if response.status_code is not 200:
            return {"Error":response.text}
        return response.json()
        
    def enable_member(self, pool_name, member_name):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool/" + pool_name + "/members/" + member_name
        self.payload = "{\n\"session\":\"user-enabled\"\n}"
        response = requests.patch(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        if response.status_code is not 200:
            return {"Error":response.text}
        return response.json()

    def member_priority(self, pool_name, member_name, priority):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/pool/" + pool_name + "/members/" + member_name
        self.payload = "{\n\"priorityGroup\":" + priority + "\n}"
        response = requests.patch(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        if response.status_code is not 200:
            return {"Error":response.text}
        return response.json()
        
    def delete_node_connections(self, node, port):
        partition = node.split('%')[1]
        self.url = "https://" + self.device_ip + "/mgmt/tm/util/bash"
        if partition == "0":
            #self.payload = "{\n    \"command\":\"run\", \n\"utilCmdArgs\": \"-c 'tmsh delete /sys connection ss-server-addr " + node + " ss-server-port " + port + "'\"\n}"
            self.payload = "{\n    \"command\":\"run\", \n\"utilCmdArgs\": \"-c 'echo \\\"delete /sys connection ss-server-addr " + node + " ss-server-port " + port + "\\\" | tmsh | bash'\"\n}"
        if partition == "1" or partition == "2" or partition == "3" or partition == "4":
            self.payload = "{\n    \"command\":\"run\", \n\"utilCmdArgs\": \"-c 'echo \\\"cd /Partition0" + partition + "; " + "delete /sys connection ss-server-addr " + node + " ss-server-port " + port + "\\\" | tmsh | bash'\"\n}"
        response = requests.post(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)

        if response.status_code is not 200:
            return {"Error":response.text}
        return response.json()

    def delete_persist_records(self, node, port):
        partition = node.split('%')[1]
        self.url = "https://" + self.device_ip + "/mgmt/tm/util/bash"
        if partition == "0":
            #self.payload = "{\n    \"command\":\"run\", \n\"utilCmdArgs\": \"-c 'tmsh delete /ltm persistence persist-records node-addr " + node + " node-port " + port + "'\"\n}"
            self.payload = "{\n    \"command\":\"run\", \n\"utilCmdArgs\": \"-c 'echo \\\"delete /ltm persistence persist-records node-addr " + node + " node-port " + port + "\\\" | tmsh | bash'\"\n}"
        if partition == "1" or partition == "2" or partition == "3" or partition == "4":
            self.payload = "{\n    \"command\":\"run\", \n\"utilCmdArgs\": \"-c 'echo \\\"cd /Partition0" + partition + "; " + "delete /ltm persistence persist-records node-addr " + node + " node-port " + port + "\\\" | tmsh | bash'\"\n}"
        response = requests.post(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        if response.status_code is not 200:
            return {"Error":response.text}
        return response.json()



    ####################################################################################################
    ### VIPs
    ####################################################################################################

    def vip_names(self):
            self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/virtual"
            vip_names = []
            vips = requests.get(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)     
            if vips.status_code is not 200:
                return {"Error":vips.text}
            else:
                for vip in vips.json()['items']:
                    tildPath = vip['fullPath'].replace('/','~')
                    vip_names.append(tildPath)
                return {"vip_names":vip_names}   

    def vip_config(self, vip_name):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/virtual/" + vip_name
        vip = requests.get(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        if vip.status_code is not 200:
            return {"Error":vip.text}
        return {"vip":vip.json()}

    def vip_stats(self, vip_name):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/virtual/" + vip_name + "/stats"
        vip_stats = requests.get(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        if vip_stats.status_code is not 200:
            return {"Error":vip_stats.text}
        return {"vip":vip_stats.json()}

    def vip_stats_filtered(self, vip_name):
        vip_stats = self.vip_stats(vip_name)
        if "Error" in vip_stats:
            return vip_stats
        vip_stats_filtered = {}

        for vs in vip_stats['vip']['entries']:
            vip_stats_filtered.update({'vip_name':vip_stats['vip']['entries'][vs]['nestedStats']['entries']['tmName']['description']})
            vip_stats_filtered.update({'address':vip_stats['vip']['entries'][vs]['nestedStats']['entries']['destination']['description']})
            vip_stats_filtered.update({'client_connections':vip_stats['vip']['entries'][vs]['nestedStats']['entries']['clientside.curConns']['value']})

        return {"vip":vip_stats_filtered}

    def vip_stats_all(self):
        self.url = "https://" + self.device_ip + "/mgmt/tm/ltm/virtual/stats"
        vip_stats_all = requests.get(self.url, data=self.payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        if vip_stats_all.status_code is not 200:
            return {"Error":vip_stats_all.text}
        return vip_stats_all.json()
    
    def vip_stats_all_filtered(self):
        dataset = []
        vip_names_all = self.vip_names()
        if "Error" in vip_names_all:
            return vip_names_all
        for vip in vip_names_all['vip_names']:
            dataset.append(self.vip_stats_filtered(vip))
            time.sleep(1)
        return {"vips":dataset}
    
    def vip_pool_stats(self, vip_name):
        # get vip stats
        vip_stats = self.vip_stats(vip_name)
        if "Error" in vip_stats:
            return vip_stats
        # get vip config in order to get the name of the pool
        vip_config = self.vip_config(vip_name)
        if "Error" in vip_config:
            return vip_config
        # get pool stats
        pool_members_stats = ""
        if 'pool' in vip_config['vip']:
            pool_name_tild = vip_config['vip']['pool'].replace('/','~')
            pool_members_stats = self.pool_members_stats(pool_name_tild)
            if "Error" in pool_members_stats:
                return pool_members_stats
        vip_pool_stats = {}
        vip_pool_stats.update(vip_stats)
        vip_pool_stats.update(pool_members_stats)
        return vip_pool_stats

    def vip_pool_stats_filtered(self, vip_name):
        # get vip stats filtered
        vip_stats_filtered = self.vip_stats_filtered(vip_name)
        if "Error" in vip_stats_filtered:
            return vip_stats_filtered
        # get vip config in order to get the name of the pool
        vip_config = self.vip_config(vip_name)
        if "Error" in vip_config:
            return vip_config
        # get pool stats
        pool_members_stats_filtered = ""
        if 'pool' in vip_config['vip']:
            pool_name_tild = vip_config['vip']['pool'].replace('/','~')
            pool_members_stats_filtered = self.pool_members_stats_filtered(pool_name_tild)
            if "Error" in pool_members_stats_filtered:
                return pool_members_stats_filtered
        vip_pool_stats_filtered = {}
        vip_pool_stats_filtered.update(vip_stats_filtered)
        vip_pool_stats_filtered.update(pool_members_stats_filtered)
        return vip_pool_stats_filtered

    def vip_pool_stats_all(self):
        dataset = []
        vip_names_all = self.vip_names()
        if "Error" in vip_names_all:
            return vip_names_all
        for vip in vip_names_all['vip_names']:
            dataset.append(self.vip_pool_stats(vip))
            time.sleep(1)
        return {"vips":dataset}

    def vip_pool_stats_all_filtered(self):
        dataset = []
        vip_names_all = self.vip_names()
        if "Error" in vip_names_all:
            return vip_names_all
        for vip in vip_names_all['vip_names']:
            dataset.append(self.vip_pool_stats_filtered(vip))
            time.sleep(1)
        return {"vips":dataset}

    

# token = getpass.getpass('token ')

# # # # # p1 = F5("x.x.x.x", "")
# # # # # token = p1.token("admin", "XXXXX")

# p = F5("10.0.0.14", token)
# print(p.pool_names())
# print(p.pool_config("~Common~walla"))
# print(p.pool_members_filtered("~Common~walla"))
# print(p.pool_members_stats("~Common~walla"))
# print(p.pool_members_stats_filtered("~Common~walla"))
# print(p.pool_members_stats_filtered_table("~Common~walla"))
# p = F5("10.0.0.14", token)
# print(p.pool_members_stats_all_filtered_table())
# print(p.disable_member("~Common~walla", "~Common~walla.co.il:443"))
# print(p.enable_member("~Common~walla", "~Common~walla.co.il:443"))
# print(p.member_priority("~Common~walla", "~Common~walla.co.il:443", "0"))




# v = F5("10.2.2.130", token)
# print(v.vip_stats_all())
# print(v.vip_stats_all_filtered())
# print(v.vip_pool_stats_all())
# print(v.vip_pool_stats_all_filtered())

