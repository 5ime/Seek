import argparse
from tools.tools import process_assets

if __name__ == "__main__":
    print('''
                      __    
  ______ ____   ____ |  | __
 /  ___// __ \_/ __ \|  |/ /
 \___ \\\\  ___/\  ___/|    < 
/____  >\___  >\___  >__|_ \\
     \/     \/     \/     \/
                version 1.0.1
                auhtor: iami233
    ''')

def print_colored_output(output, item):
    color_code = '\033[32m' 
    if '疑似站群' in item[1]:
        color_code = '\033[31m'
    elif '未备案' in item[2]:
        color_code = '\033[33m'
    reset_code = '\033[0m'
    colored_output = '{}{}{}'.format(color_code, output, reset_code)
    print(colored_output)

description = "此工具允许您执行与IP和域名相关的操作，包括同IP站点查找和域名信息查询。\nExample: python main.py -file assets.txt"
parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-file", dest="file_path", help="Path to the assets file")
args = parser.parse_args()

try:
    data = process_assets(args.file_path)
    print('[+] 目标\t资产\t备案信息\t权重信息')
    for item in data:
        record = item[2]
        record_value = record[0] if isinstance(record, tuple) else record
        pr_value = record[1] if isinstance(record, tuple) else None
        baidu_pc_value = record[2][0] if isinstance(record, tuple) and len(record) > 2 else None
        baidu_mobile_value = record[2][1] if isinstance(record, tuple) and len(record) > 2 else None

        output = '[+] {}\t{}\t{}\t{}\t{}\t{}'.format(item[0], item[1], record_value, pr_value, baidu_pc_value, baidu_mobile_value)
        print_colored_output(output, item)
except:
    parser.print_help()
