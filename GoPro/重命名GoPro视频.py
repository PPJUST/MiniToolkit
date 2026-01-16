"""
名称：重命名GoPro视频
版本号：v1.0
更新日期：2026.01.16
功能：规范的重命名GoPro的视频文件
使用方法：按提示操作即可
其他说明：GoPro 摄像机的文件命名规则https://community.gopro.com/s/article/GoPro-Camera-File-Naming-Convention?language=zh_CN
"""
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
循环录像 GHYYxxxx.mp4 GHAA0001.mp4、GHAA0002.mp4
        GXYYxxxx.mp4
"""