"""
名称：删除失效快捷方式
版本号：v1.1
更新日期：2026.01.22
功能：删除一个文件夹中指向路径无效的快捷方式
使用方法：打开后，输入对应代码并回车后执行操作
其他说明：
"""
import sys

print(__doc__ if __doc__ else "该文件未定义描述信息")
print('-' * 20)

import configparser
import os

import send2trash
import win32com.client


def get_original_path(shortcut_path):
    """获取一个快捷方式指向的路径"""
    try:
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        return shortcut.Targetpath
    except Exception as e:
        return f"Error: {e}"


def check_config():
    """检查配置文件是否存在，如不存在则新建"""
    if not os.path.exists('config.ini'):
        with open('config.ini', 'w') as cw:
            the_settings = """[DEFAULT]
check_dirpath = 
    """
            cw.write(the_settings)


def get_config_setting(key: str) -> str:
    """获取配置文件中指定key的value"""
    config = configparser.ConfigParser()
    config.read('config.ini')

    return config.get('DEFAULT', key)


def set_check_folder(_dirpath: str):
    """设置需要检查的文件夹路径"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set('DEFAULT', 'check_dirpath', _dirpath)
    config.write(open('config.ini', 'w'))


def check_dirpath(_dirpath: str):
    """检查文件夹"""
    if not _dirpath or not os.path.exists(_dirpath):
        print(f'指定路径不存在：{_dirpath}')
        return

    for filename in os.listdir(_dirpath):
        fullpath = os.path.join(_dirpath, filename)
        if os.path.isfile(fullpath) and fullpath.lower().endswith('.lnk') and os.path.getsize(fullpath) < 1048576:
            original_path = get_original_path(fullpath)
            print(f'---【{filename}】 的指向文件路径为 【{original_path}】')
            if not os.path.exists(original_path):
                send2trash.send2trash(fullpath)
                print(f'======指向路径不存在，已删除 【{filename}】')
    print('已检查所有快捷方式')


if __name__ == '__main__':
    check_config()
    dirpath = get_config_setting('check_dirpath')

    while True:
        info = f"""
--------------------
上次检查的文件夹路径：{dirpath}

输入代码并回车后执行相应操作：
【文件夹路径】设置文件夹路径
【1】执行检查
【2】退出
--------------------
            """
        print(info)
        input_code = input('输入代码：')
        if os.path.exists(input_code) and os.path.isdir(input_code):
            dirpath = input_code
            set_check_folder(dirpath)
        elif input_code == '1':
            check_dirpath(dirpath)
        elif input_code == '2':
            sys.exit()
        else:
            print('输入错误')
