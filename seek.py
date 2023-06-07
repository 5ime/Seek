import argparse
from tools.tools import *
if __name__ == "__main__":
    print('''
                      __    
  ______ ____   ____ |  | __
 /  ___// __ \_/ __ \|  |/ /
 \___ \\\\  ___/\  ___/|    < 
/____  >\___  >\___  >__|_ \\
     \/     \/     \/     \/
                version 1.0.2
                auhtor: iami233
    ''')

    description = "此工具允许您执行与IP和域名相关的操作，包括同IP站点查找和域名信息查询。\nExample: python main.py -file assets.txt"
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-file", dest="file_path", help="Path to the assets file")
    args = parser.parse_args()

    try:
       data = process_assets(args.file_path)
    except:
        parser.print_help()