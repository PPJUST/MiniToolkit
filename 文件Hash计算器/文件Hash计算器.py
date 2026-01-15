"""
名称：文件Hash计算器
版本号：v1.2
更新日期：2026.01.15
功能：计算文件的MD5和SHA-256哈希值
使用方法：打包为可执行文件后，将文件拖入可执行文件即可
其他说明：仅支持拖入执行，不支持直接打开使用
"""
import hashlib
import os
import sys


def calc_md5(filepath: str):
    _md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            _md5.update(chunk)
    return _md5.hexdigest()


def calc_sha256(filepath: str):
    _sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            _sha256.update(chunk)
    return _sha256.hexdigest()


try:
    drop_paths = sys.argv[1:]
except IndexError:
    drop_paths = []

print(__doc__ if __doc__ else "该文件未定义描述信息")
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
