"""
名称：更新Github加速Hosts
版本号：v1.1
更新日期：2026.01.23
功能：更新Hosts，加速访问Github
使用方法：按提示操作即可
其他说明：
"""
import subprocess
import sys
from typing import Union

import pythoncom
import requests
import win32com.shell.shell as shell

print(__doc__ if __doc__ else "该文件未定义描述信息")
print('-' * 20)

_Hosts_File = r'C:\Windows\System32\drivers\etc\hosts'
_Hosts_URL_FetchGitHub = 'https://hosts.gitcdn.top/hosts.txt'
_Hosts_URL_Github520 = 'https://raw.hellogithub.com/hosts'


def run_as_admin():
    shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=' '.join(sys.argv), nShow=1)


def read_local_hosts() -> list:
    """读取本地hosts文件"""
    with open(_Hosts_File, 'r', encoding='utf-8') as f:
        hosts_local = f.readlines()

    return hosts_local


def clear_local_github_hosts():
    """删除本地hosts文件中的github相关host"""
    local_hosts = read_local_hosts()
    new_hosts = local_hosts

    # 删除FetchGitHub
    if '# fetch-github-hosts begin\n' in new_hosts:
        begin = new_hosts.index('# fetch-github-hosts begin\n')
        end = new_hosts.index('# fetch-github-hosts end\n')
        new_hosts = new_hosts[:begin] + new_hosts[end + 1:]
    # 删除GitHub520
    if '# GitHub520 Host Start\n' in new_hosts:
        begin = new_hosts.index('# GitHub520 Host Start\n')
        end = new_hosts.index('# GitHub520 Host End\n')
        new_hosts = new_hosts[:begin] + new_hosts[end + 1:]

    with open(_Hosts_File, 'w', encoding='utf-8') as hw:
        hw.writelines(new_hosts)

    flush_dns()


def flush_dns():
    """刷新DNS缓存"""
    subprocess.run(['ipconfig', '/flushdns'], shell=True)


def read_url_hosts(url) -> Union[list, None]:
    """读取网络hosts文件"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    hosts_html = response.text

    if not hosts_html:
        return None

    hosts_html_list = hosts_html.splitlines()
    hosts_html_list = [i + '\n' for i in hosts_html_list]

    return hosts_html_list


def add_local_hosts(hosts_list: list):
    """添加host到本地hosts"""
    if hosts_list:
        clear_local_github_hosts()
        local_hosts = read_local_hosts()

        join_hosts = local_hosts + ['\n'] + hosts_list

        with open(_Hosts_File, 'w', encoding='utf-8') as hw:
            hw.writelines(join_hosts)  # 注意 列表中的每一个元素后都需要有\n换行符

        flush_dns()


if __name__ == '__main__':
    # 检查管理员权限
    if not shell.IsUserAnAdmin():
        run_as_admin()
    pythoncom.CoUninitialize()

    while True:
        _code = input(
            '输入对应代码后回车执行：\n1.更新FetchGitHub\n2.更新GitHub520\n3.清除Github相关host\n4.退出\n在此输入：')
        if _code == '1':
            print('正在更新Hosts-FetchGitHub')
            _hosts_list = read_url_hosts(_Hosts_URL_FetchGitHub)
            add_local_hosts(_hosts_list)
            print('更新完成')
        elif _code == '2':
            print('正在更新Hosts-GitHub520')
            _hosts_list = read_url_hosts(_Hosts_URL_Github520)
            add_local_hosts(_hosts_list)
            print('更新完成')
        elif _code == '3':
            print('正在清除Github相关host')
            clear_local_github_hosts()
            print('清除完成')
        elif _code == '4':
            print('退出')
            exit()

        print('-' * 20)
