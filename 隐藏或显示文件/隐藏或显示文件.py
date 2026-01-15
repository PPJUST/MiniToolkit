"""
名称：隐藏或显示文件
版本号：v1.0
更新日期：2026.01.15
功能：隐藏或显示文件和文件夹（设置隐藏属性）
使用方法：输入文件路径后，选择显示或隐藏
其他说明：
"""
print(__doc__ if __doc__ else "该文件未定义描述信息")
print('-' * 20)

import os
import subprocess


def walk_path(path):
    """遍历路径，获取内部所有文件和文件夹"""
    if not os.path.exists(path):
        return []

    if os.path.isfile(path):
        return [path]
    else:
        insides = set()
        insides.add(path)
        for dirpath, dirnames, filenames in os.walk(path):
            for j in filenames:
                filepath_join = os.path.normpath(os.path.join(dirpath, j))
                insides.add(filepath_join)

            for k in dirnames:
                dirpath_join = os.path.normpath(os.path.join(dirpath, k))
                insides.add(dirpath_join)

        return insides


if __name__ == '__main__':
    while True:
        _path = input('输入文件/文件夹路径：')
        is_hidden = input('输入对应字符 H:隐藏/S:显示：').lower() == 'H'
        _insides = walk_path(_path)
        if is_hidden:
            for i in _insides:
                subprocess.run(['attrib', '+h', i])
                print('已隐藏：', i)
        else:
            for i in _insides:
                subprocess.run(['attrib', '-h', i])
                print('已显示：', i)
