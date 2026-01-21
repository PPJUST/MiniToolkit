"""
名称：重命名GoPro视频
版本号：v1.0
更新日期：2026.01.21
功能：规范的重命名GoPro的视频文件
使用方法：按提示操作即可
其他说明：GoPro 摄像机的文件命名规则https://community.gopro.com/s/article/GoPro-Camera-File-Naming-Convention?language=zh_CN
"""
import os
import re
from typing import List, Dict

print(__doc__ if __doc__ else "该文件未定义描述信息")
print('-' * 20)

"""
GoPro视频命名规则
zz 章节编号
xxxx 文件编号
H AVC编码
X HEVC编码

HERO 5 及之前型号
单个视频 GOPRxxxx.mp4 GOPR1234.mp4
分段视频 首个视频GOPRxxxx.mp4 GOPR1234.mp4
        其余章节GPzzxxxx.mp4 GP011234.mp4、GP021234.mp4

HERO 6 及之后型号
单个视频 GH01xxxx.mp4 GH011234.mp4
        GX01xxxx.mp4 GX011234.mp4
分段视频 GHzzxxxx.mp4 GH011234.mp4、GH021234.mp4
        GXzzxxxx.mp4
"""

# 正则表达式
Pattern_Old_Single = r'GOPR(\d{4})'  # GOPR1234.mp4
Pattern_Old_Chaptered = r'GP(\d{2})(\d{4})'  # GP021234.mp4
Pattern_New_Single_AVC = r'GH(\d{2})(\d{4})'  # GH011234.mp4
Pattern_New_Single_HAVC = r'GX(\d{2})(\d{4})'  # GX011234.mp4
Pattern_New_Chaptered_AVC = Pattern_New_Single_AVC  # GH021234.mp4
Pattern_New_Chaptered_HAVC = Pattern_New_Single_HAVC  # GH021234.mp4


def guess_first_chaptered_name(name: str) -> str:
    """猜测传入的视频文件名可能的首个分段视频文件名，用于分组"""
    if re.match(Pattern_Old_Single, name):
        number = re.match(Pattern_Old_Single, name).group(1)
        guess_name = f'GOPR{number}'
        return guess_name
    elif re.match(Pattern_Old_Chaptered, name):
        number = re.match(Pattern_Old_Chaptered, name).group(2)
        guess_name = f'GOPR{number}'
        return guess_name
    elif re.match(Pattern_New_Single_AVC, name):
        number = re.match(Pattern_New_Single_AVC, name).group(2)
        guess_name = f'GH01{number}'
        return guess_name
    elif re.match(Pattern_New_Single_HAVC, name):
        number = re.match(Pattern_New_Single_HAVC, name).group(2)
        guess_name = f'GX01{number}'
        return guess_name
    elif re.match(Pattern_New_Chaptered_AVC, name):
        number = re.match(Pattern_New_Chaptered_AVC, name).group(2)
        guess_name = f'GH01{number}'
        return guess_name
    elif re.match(Pattern_New_Chaptered_HAVC, name):
        number = re.match(Pattern_New_Chaptered_HAVC, name).group(2)
        guess_name = f'GX01{number}'
        return guess_name

    return ''


def standardized_name(name: str) -> str:
    """标准化文件，将视频编号提前"""
    if re.match(Pattern_Old_Single, name):
        chapter = '00'
        number = re.match(Pattern_Old_Single, name).group(1)
    elif re.match(Pattern_Old_Chaptered, name):
        chapter, number = re.match(Pattern_Old_Chaptered, name).groups()
    elif re.match(Pattern_New_Single_AVC, name):
        chapter, number = re.match(Pattern_New_Single_AVC, name).groups()
    elif re.match(Pattern_New_Single_HAVC, name):
        chapter, number = re.match(Pattern_New_Single_HAVC, name).groups()
    elif re.match(Pattern_New_Chaptered_AVC, name):
        chapter, number = re.match(Pattern_New_Chaptered_AVC, name).groups()
    elif re.match(Pattern_New_Chaptered_HAVC, name):
        chapter, number = re.match(Pattern_New_Chaptered_HAVC, name).groups()
    else:
        chapter, number = None, None

    if chapter and number:
        new_name = f'{number}_{chapter}_{name}'
        return new_name
    else:
        return ''


def class_names(names: List[str]) -> List[str]:
    """将传入的文件名列表进行分组，将统一编号的文件名分在同一组中"""
    class_dict = dict()
    for name in names:
        guess_first_name = guess_first_chaptered_name(name)
        if guess_first_name:
            if guess_first_name not in class_dict:
                class_dict[guess_first_name] = []
            class_dict[guess_first_name].append(name)

    return list(class_dict.values())


def rename_files(filepaths: List[str]):
    """批量重命名文件"""
    print('生成预修改的文件名')
    # 生成文件路径和新文件名的字典
    file_dict: Dict[str, str] = dict()
    for filepath in filepaths:
        file_dict[filepath] = ''
        filename = os.path.basename(filepath)
        filetitle, extension = os.path.splitext(filename)
        new_filetitle = standardized_name(filetitle)
        if new_filetitle:
            new_filename = new_filetitle + extension
            file_dict[filepath] = new_filename
            print(f'原文件名：{filename} -> {new_filename}')
        else:
            pass

    # 再次确认是否需要重命名
    is_rename = input('是否执行重命名？(Y/N)：')
    if is_rename.upper() == 'Y':
        for filepath, new_filename in file_dict.items():
            if new_filename:
                new_filepath = os.path.join(os.path.dirname(filepath), new_filename)
                new_filepath = os.path.normpath(new_filepath)
                os.rename(filepath, new_filepath)
                print(f'重命名成功：{filepath} -> {new_filename}')
            else:
                print(f'文件名未修改：{filepath}')

    print('重命名完成')


def get_files(path: str) -> List[str]:
    """获取指定目录下的所有文件"""
    filepaths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            filepath = os.path.normpath(filepath)
            filepaths.append(filepath)

    return filepaths


if __name__ == '__main__':
    input_path = input('输入GoPro视频所在的文件夹路径：')
    if os.path.exists(input_path) and os.path.isdir(input_path):
        _files = get_files(input_path)
        rename_files(_files)

        print('-' * 20)
        input("\n完成！输入回车后退出...")
    else:
        print("传入路径错误")
        input("\n输入回车后退出...")