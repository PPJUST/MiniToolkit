"""
名称：文件Hash计算器
版本号：v1.0
更新日期：2026.01.04
功能：计算文件的MD5和SHA-256哈希值
使用方法：打包为可执行文件后，将文件拖入可执行文件即可
其他说明：仅支持拖入执行，不支持直接打开使用
"""

import os
import sys

import lzytools


def calc_md5(filepath: str):
    md5 = lzytools.file.calc_md5_from_file(filepath)
    return md5


def calc_sha256(filepath: str):
    sha256 = lzytools.file.calc_sha256_from_file(filepath)
    return sha256


try:
    drop_paths = sys.argv[1:]
except IndexError:
    drop_paths = []

print("""名称：文件Hash计算器
版本号：v1.0
更新日期：2026.01.04
功能：计算文件的MD5和SHA-256哈希值
使用方法：打包为可执行文件后，将文件拖入可执行文件即可
其他说明：仅支持拖入执行，不支持直接打开使用""")
print('-' * 20)

if drop_paths:
    for path in drop_paths:
        if os.path.exists(path) and os.path.isfile(path):
            print('filepath:', path)
            md5 = calc_md5(path)
            print('MD5:', md5)
            sha256 = calc_sha256(path)
            print('SHA-256:', sha256)
            print('-' * 20)

    input("\n计算完成！输入回车后退出...")
else:
    print("请将文件拖入可执行文件！不支持直接打开使用")
    input("\n输入回车后退出...")
