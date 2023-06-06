import re
import time
from utils.utils import fetch_record, find_related_sites, saveExcel

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
    domains = set()
    ips = set()
    list = []

    with open(file_path, "r") as file:
        lines = file.readlines()

    domains, ips = process_lines(lines)

    for domain in domains:
        domains = fetch_record(domain)
        list.append((domain, '暂无', domains))
        time.sleep(1)

    for ip in ips:
        domain_set = find_related_sites(ip)
        if isinstance(domain_set, set):
            related_domains, _ = process_lines(domain_set)
            for domain in related_domains:
                icp = fetch_record(domain)
                time.sleep(1)
                list.append((ip, domain, icp))
        else:
            list.append((ip, domain_set, '暂无'))

    saveExcel(list)
    return list