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

def fetch_record(domain):
    unitname = getUnitname(domain)
    pagerank = getPagerank(domain)
    rank = getRank(domain)
    return unitname, pagerank, rank

def find_related_sites(ip):
    return getWebsite(ip)

def getPagerank(domain):
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

def getRank(domain):
    token = '' # 这里填写你的token
    url = 'https://apistore.aizhan.com/baidurank/siteinfos/{}?domains={}'.format(token, domain)
    header = {
        "User-Agent": ua.random,
        "Referer": "https://www.aizhan.com/",
        "Origin": "https://www.aizhan.com/",
        "CLIENT-IP": ip,
        "X-FORWARDED-FOR": ip
    }
    try:
        result = session.get(url, headers=header, verify=False).text
        pcRank = json.loads(result)['data']['success'][0]['pc_br']
        mobileRank = json.loads(result)['data']['success'][0]['m_br']
        return pcRank, mobileRank
    except:
        return '无法获取'

def getWebsite(ip):
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

def getToken():
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
    result = session.post(url, headers=header, data=data, timeout=5, verify=False).text
    return json.loads(result)['params']['bussiness']

try:
    token = getToken()
except:
    token = ''

def getUuid():
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
    

def getUnitname(name):
    url = "https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition"
    try:
        header = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "uuid": getUuid(),
            "token": token,
            "Origin": "https://beian.miit.gov.cn/",
            "Referer": "https://beian.miit.gov.cn/"
        }
        data = { "pageNum": "1", "pageSize": "100", "unitName": name }
        result = session.post(url, headers=header, json=data, verify=False).text
        unitName = json.loads(result)['params']['list'][0]['unitName']
        return unitName
    except:
        return "未备案"

def saveExcel(data):
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