"""
名称：空文件夹搜索器
版本号：v1.0
更新日期：2026.05.10
功能：搜索一个文件夹下的空文件夹，可选择删除搜索到的空文件夹
使用方法：按提示操作即可
其他说明：
"""
import lzytools.file
import send2trash

print(__doc__ if __doc__ else "该文件未定义描述信息")
print('-' * 20)

import os


def find_empty_folders(check_path: str):
    """搜索空文件夹"""
    empty_folders = lzytools.file.find_empty_folder(check_path)

    return empty_folders


if __name__ == '__main__':
    while True:
        input_path = input('输入需要检查的文件夹路径：')
        if os.path.exists(input_path) and os.path.isdir(input_path):
            empty_folders = lzytools.file.find_empty_folder(input_path)

            if empty_folders:
                print('搜索到以下空文件夹：')
                print('\n'.join(empty_folders))
            else:
                print('未搜索到空文件夹')

            is_delete = input('是否删除空文件夹：Y/N ')
            is_delete = is_delete.upper()

            if is_delete == 'Y':
                for i in empty_folders:
                    if os.path.exists(i):
                        send2trash.send2trash(i)
                        print(f'已删除： {i}')
                    else:
                        print(f'路径不存在，已跳过： {i}')
                print('已删除全部空文件夹')
            elif is_delete == 'N':
                pass
            else:
                print('传入参数错误')

            print('-' * 20)

        else:
            print("传入路径错误")
