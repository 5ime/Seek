import re
import time
import json
import random
import urllib3
import hashlib
import requests
import fake_useragent
from openpyxl import Workbook

urllib3.disable_warnings()
session = requests.Session()
ua = fake_useragent.UserAgent()
ip = f"101.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

TOKEN = "" # 请填写您的爱站接口私钥

def fetch_record(domain):
    unitname = get_unitname(domain)
    pagerank = get_pagerank(domain)
    rank = get_rank(domain)
    return unitname, pagerank, rank

def find_related_sites(ip):
    return get_website(ip)

def get_pagerank(domain):
    url = "https://pr.aizhan.com/{}/".format(domain)
    header = {
        "User-Agent": ua.random,
        "Referer": "https://www.aizhan.com/",
        "Origin": "https://www.aizhan.com/",
        "CLIENT-IP": ip,
        "X-FORWARDED-FOR": ip
    }
    try:
        result = session.get(url, headers=header, verify=False).text
        pr = re.search(r'<span>谷歌PR：</span><a><img src="//statics.aizhan.com/images/pr/(.*?).png" alt=".*?"/></a>', result).group(1)
        return pr
    except:
        return '无法获取'

def get_rank(domain):
    url = 'https://apistore.aizhan.com/baidurank/siteinfos/{}?domains={}'.format(TOKEN, domain)
    header = {
        "User-Agent": ua.random,
        "Referer": "https://www.aizhan.com/",
        "Origin": "https://www.aizhan.com/",
        "CLIENT-IP": ip,
        "X-FORWARDED-FOR": ip
    }
    try:
        result = session.get(url, headers=header, verify=False).text
        pc_rank = json.loads(result)['data']['success'][0]['pc_br']
        mobile_rank = json.loads(result)['data']['success'][0]['m_br']
        return pc_rank, mobile_rank
    except:
        return '无法获取'

def get_website(ip):
    url = "https://api.webscan.cc/?action=query&ip=" + ip
    header = {
        "User-Agent": ua.random,
        "Referer": "https://webscan.cc/",
        "Origin": "https://webscan.cc/",
        "CLIENT-IP": ip,
        "X-FORWARDED-FOR": ip
    }
    try:
        domains = set()
        result = json.loads(session.get(url, headers=header, verify=False).text)
        for i in result:
            domains.add(i['domain'])
        if len(domains) > 5:
            return '疑似站群'
        return domains
    except:
        return '无同IP网站'

def get_token():
    timeStamp = int(time.time())
    authKey = hashlib.md5(("testtest" + str(timeStamp)).encode()).hexdigest()
    url = "https://hlwicpfwc.miit.gov.cn/icpproject_query/api/auth"
    data = { "authKey": authKey, "timeStamp": timeStamp }
    header = {
        "Origin": "https://beian.miit.gov.cn/",
        "Referer": "https://beian.miit.gov.cn/",
        "User-Agent": ua.random,
        "CLIENT-IP": ip,
               "X-FORWARDED-FOR": ip
    }
    try: 
        result = session.post(url, headers=header, data=data, timeout=5, verify=False).text
        return json.loads(result)['params']['bussiness']
    except:
        return ''

token = get_token()

def get_uuid():
    url = "https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImage"
    header = {
        "Origin": "https://beian.miit.gov.cn/",
        "Referer": "https://beian.miit.gov.cn/",
        "User-Agent": ua.random,
        "token": token
    }
    result = session.get(url, headers=header, timeout=5, verify=False).text
    uuid = json.loads(result)['params']['uuid']
    return uuid

def get_unitname(name):
    url = "https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition"
    try:
        header = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": ua.random,
            "Accept": "application/json, text/plain, */*",
            "uuid": get_uuid(),
            "token": token,
            "Origin": "https://beian.miit.gov.cn/",
            "Referer": "https://beian.miit.gov.cn/"
        }
    except:
        return get_unitname2(name)
    
    try:
        data = { "pageNum": "1", "pageSize": "100", "unitName": name }
        result = session.post(url, headers=header, json=data, verify=False).text
        unitName = json.loads(result)['params']['list'][0]['unitName']
        return unitName
    except:
        return "未备案"

def get_unitname2(name):
    url = 'https://api.emoao.com/api/icp?domain=' + name
    header = {
        "User-Agent": ua.random,
        "Referer": "https://api.emoao.com/",
        "Origin": "https://api.emoao.com/",
        "CLIENT-IP": ip,
        "X-FORWARDED-FOR": ip
    }
    try:
        result = session.get(url, headers=header, verify=False).text
        unitName = json.loads(result)['unitName'] if json.loads(result)['unitName'] else '未备案'
        return unitName
    except:
        return "查询失败"

def save_excel(data):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(['目标', '资产', '备案', '谷歌PR', 'PC百度权重', '移动百度权重'])

    for item in data:
        domain, asset, record = item[0], item[1], item[2]
        record_value = record[0] if isinstance(record, tuple) else record
        pr_value = record[1] if isinstance(record, tuple) else None
        baidu_pc_value = record[2][0] if isinstance(record, tuple) and len(record) > 2 else None
        baidu_mobile_value = record[2][1] if isinstance(record, tuple) and len(record) > 2 else None

        row_data = [domain, asset, record_value, pr_value, baidu_pc_value, baidu_mobile_value]
        sheet.append(row_data)

    workbook.save('results.xlsx')

