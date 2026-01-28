"""
名称：PDF图片互转器
版本号：v1.1
更新日期：2026.01.28
功能：将PDF转为图片，将图片合并为一个PDF
使用方法：打包为可执行文件后，将文件拖入可执行文件即可
其他说明：仅支持拖入执行，不支持直接打开使用；拖入图片时执行合并为PDF操作，拖入PDF时执行转为图片操作
"""
import time

print(__doc__ if __doc__ else "该文件未定义描述信息")
print('-' * 20)

import os
import sys

import filetype
import fitz


def pdf_to_image(pdf_path: str):
    """将PDF每页导出为图片"""
    print(f'导出PDF为图片：{pdf_path}')
    doc = fitz.open(pdf_path)
    # 根据页数分别处理，如果是单页则直接导出图片，如果为多页则导出到一个文件夹中
    pages_count = doc.page_count
    filetitle = os.path.basename(os.path.splitext(pdf_path)[0])
    dirpath = os.path.dirname(pdf_path)
    if pages_count == 1:
        pix = doc[0].get_pixmap(dpi=300)
        pix.save(f'{dirpath}/{filetitle}.png')
    elif pages_count > 1:
        os.mkdir(f'{dirpath}/{filetitle}')
        for index, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=300)
            pix.save(f'{dirpath}/{filetitle}/{index}.png')
    print(f'完成导出：{dirpath}')


def image_to_pdf(_images: list, output: str = 'output.pdf'):
    """将图片合并为PDF"""
    print(f'合并图片：{_images}')
    merged_pdf = fitz.open()  # 最终合并的PDF

    for image_file in _images:
        # 读取图片，转为PDF流
        img = fitz.open(image_file)
        # rect = img[0].rect  # 读取图片尺寸
        pdf_bytes = img.convert_to_pdf()
        img.close()
        # 读取PDF流，转为PDF对象
        img_page = fitz.open("pdf", pdf_bytes)
        # 插入
        merged_pdf.insert_pdf(img_page)

    dirpath = os.path.dirname(_images[0])
    merged_pdf.save(f'{dirpath}/{output}')
    print(f'完成合并：{dirpath}/{output}')
    merged_pdf.close()


def is_image(file: str):
    """文件是否是图片"""
    return filetype.is_image(file)


def is_pdf(file: str):
    """文件是否是pdf"""
    kind = filetype.guess(file)
    if kind is None:
        return False

    guess_type = kind.extension
    if guess_type == 'pdf':
        return True
    else:
        return False


def get_files(folder: str):
    """获取文件夹下所有文件路径"""
    _files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for j in filenames:
            filepath_join = os.path.normpath(os.path.join(dirpath, j))
            _files.append(filepath_join)

    return _files


if __name__ == '__main__':
    try:
        drop_paths = sys.argv[1:]
    except IndexError:
        drop_paths = []

    if drop_paths:
        # 收集全部文件
        files = []
        for path in drop_paths:
            if os.path.isfile(path):
                files.append(path)
            else:
                walks = get_files(path)
                files += walks

        # 按文件类型提取不同分类的文件路径
        images = [i for i in files if is_image(i)]
        pdfs = [i for i in files if is_pdf(i)]

        # 如果同时存在图片和pdf，则不做处理直接退出
        if images and pdfs:
            print("同时存在图片和PDF，请重新选择！")
        else:
            if images:  # 执行图片合并为一个PDF操作
                image_to_pdf(images)
            elif pdfs:  # 执行PDF转为图片操作
                for pdf in pdfs:
                    pdf_to_image(pdf)

        print('-' * 20)
        print("\n完成！5秒后退出...")
        time.sleep(5)
    else:
        print("请将文件拖入可执行文件！不支持直接打开使用")
        print("\n5秒后退出...")
        time.sleep(5)
