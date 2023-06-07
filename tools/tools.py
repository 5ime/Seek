import re
import time
from utils.utils import *

def process_lines(lines):
    domains = set()
    ips = set()
    domain_pattern = re.compile(r"(?:https?://)?([\w.-]+\.[a-zA-Z]{2,}\b)")
    ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

    for line in lines:
        line = line.strip()
        domain_match = re.search(domain_pattern, line)
        ip_match = re.search(ip_pattern, line)

        if domain_match:
            domain = domain_match.group(1)
            domain_parts = domain.split('.')
            root_domain = '.'.join(domain_parts[-3:]) if len(domain_parts) > 2 and domain_parts[-2] in ['edu', 'gov', 'org', 'com'] else '.'.join(domain_parts[-2:])
            domains.add(root_domain)

        if ip_match:
            ips.add(ip_match.group())

    return domains, ips

def process_assets(file_path):
    print('[+] 目标\t资产\t备案信息\t权重信息')

    list = []

    with open(file_path, "r") as file:
        lines = file.readlines()

    domains, ips = process_lines(lines)

    for domain in domains:
        record = fetch_record(domain)
        list.append((domain, '暂无', record))
        time.sleep(1)
        print_result((domain, '暂无', record))

    for ip in ips:
        domain_set = find_related_sites(ip)
        if isinstance(domain_set, set):
            related_domains, _ = process_lines(domain_set)
            for domain in related_domains:
                record = fetch_record(domain)
                time.sleep(1)
                print_result((ip, domain, record))
                list.append((ip, domain, record))
        else:
            print_result((ip, domain_set, '暂无'))
            list.append((ip, domain_set, '暂无'))

    save_excel(list)
    return list

def print_result(item):
    record = item[2]
    record_value = record[0] if isinstance(record, tuple) else record
    pr_value = record[1] if isinstance(record, tuple) else None
    baidu_pc_value = record[2][0] if isinstance(record, tuple) and len(record) > 2 else None
    baidu_mobile_value = record[2][1] if isinstance(record, tuple) and len(record) > 2 else None

    output = '[+] {}\t{}\t{}\t{}\t{}\t{}'.format(item[0], item[1], record_value, pr_value, baidu_pc_value, baidu_mobile_value)
    print_colored_output(output, item)


def print_colored_output(output, item):
    color_code = '\033[32m'
    if '疑似站群' in item[1]:
        color_code = '\033[31m'
    elif '未备案' in item[2]:
        color_code = '\033[33m'
    reset_code = '\033[0m'
    colored_output = '{}{}{}'.format(color_code, output, reset_code)
    print(colored_output)