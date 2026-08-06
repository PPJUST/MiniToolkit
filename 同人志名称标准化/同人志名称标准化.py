"""
名称：同人志名称标准化
版本号：v0.1
更新日期：2026.08.06
功能：标准化同人志的文件名
使用方法：拖入同人志文件夹/压缩文件到可执行程序图标上
其他说明：

"""
import os
import sys
import time

import lzytools

print(__doc__ if __doc__ else "该文件未定义描述信息")
print('-' * 20)

import DoujinTools


def analyse_filetitle(filetitle: str):
    doujin = DoujinTools.name.DoujinshiName(filetitle)

    return doujin


def get_filetitle(filepath: str):
    """提取文件标题"""
    if os.path.exists(filepath):
        if os.path.isdir(filepath):
            filetitle = os.path.split(filepath)[1]
        else:
            filetitle = os.path.split(os.path.splitext(filepath)[0])[1]
    else:
        filetitle = os.path.split(filepath)[1]

    return filetitle


if __name__ == '__main__':
    try:
        drop_paths = sys.argv[1:]
    except IndexError:
        drop_paths = []

    if drop_paths:
        print(f'共拖入{len(drop_paths)}个文件路径')
        print('-' * 10)

        for index, path in enumerate(drop_paths, start=1):
            print(f'处理第{index}个文件：{path}')
            print('--分析文件名信息')
            _filetitle = get_filetitle(path)
            _dirpath = os.path.dirname(path)
            doujin_class = analyse_filetitle(_filetitle)
            doujin_class.print_information()

            if doujin_class.is_match_pattern:
                print('--文件名符合标准，支持标准化重命名')
                t_name = doujin_class.get_normalized_name()
                if t_name == _filetitle:
                    print('--文件名已标准化，无需重命名')
                else:
                    print(f'标准化文件名预览：{t_name}')
                    is_rn = input('是否重命名？Y/N').upper()
                    if is_rn == 'Y':
                        if os.path.isfile(path):
                            extension = os.path.splitext(path)[1]
                        else:
                            extension = None
                        new_filename_no_dup = lzytools.file.create_nodup_filename_custom_suffix(t_name, _dirpath, '@@',
                                                                                                extension)
                        new_path = os.path.join(_dirpath, new_filename_no_dup)
                        os.rename(path, new_path)
                        print(f'已将文件重命名为：{new_filename_no_dup}')
            else:
                print('--文件名不符合标准，不支持标准化重命名')

            print('-' * 10)

        print('-' * 20)
        print("\n完成！5秒后退出...")
        time.sleep(5)
    else:
        print("请将文件拖入可执行文件！不支持直接打开使用")
        print("\n5秒后退出...")
        time.sleep(5)
