"""
名称：重命名GoPro视频
版本号：v1.0
更新日期：2026.01.16
功能：规范的重命名GoPro的视频文件
使用方法：按提示操作即可
其他说明：GoPro 摄像机的文件命名规则https://community.gopro.com/s/article/GoPro-Camera-File-Naming-Convention?language=zh_CN
"""
import re
from typing import List

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
        chapter = '01'
        number = re.match(Pattern_Old_Single, name).group(1)
    elif re.match(Pattern_Old_Chaptered, name):
        chapter, number = re.match(Pattern_Old_Chaptered, name).group()
    elif re.match(Pattern_New_Single_AVC, name):
        chapter, number = re.match(Pattern_New_Single_AVC, name).group()
    elif re.match(Pattern_New_Single_HAVC, name):
        chapter, number = re.match(Pattern_New_Single_HAVC, name).group()
    elif re.match(Pattern_New_Chaptered_AVC, name):
        chapter, number = re.match(Pattern_New_Chaptered_AVC, name).group()
    elif re.match(Pattern_New_Chaptered_HAVC, name):
        chapter, number = re.match(Pattern_New_Chaptered_HAVC, name).group()
    else:
        chapter, number =None,None

    if chapter and number:
        new_name = f'{number}_{chapter}_{name}'
        return new_name

def class_names(names:List[str])->List[str]:
    """将传入的文件名列表进行分组，将统一编号的文件名分在同一组中"""
    class_dict = dict()
    for name in names:
        guess_first_name = guess_first_chaptered_name(name)
        if guess_first_name:
            if guess_first_name not in class_dict:
                class_dict[guess_first_name] = []
            class_dict[guess_first_name].append(name)

    return list(class_dict.values())



