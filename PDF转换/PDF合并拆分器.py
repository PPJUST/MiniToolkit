"""
名称：PDF拆分合并
版本号：v1.0
更新日期：2026.01.15
功能：拆分一个PDF为单独的文件，合并多个PDF为一个文件
使用方法：打包为可执行文件后，将文件拖入可执行文件即可
其他说明：仅支持拖入执行，不支持直接打开使用；拖入单个文件时执行拆分操作，拖入多个文件时执行合并操作
"""
print(__doc__ if __doc__ else "该文件未定义描述信息")
print('-' * 20)

import os
import sys

import filetype
import fitz


def merge_pdfs(pdfs_path: list, output: str = 'output.pdf'):
    """合并多个PDF"""
    print(f'合并：{pdfs_path}')
    merged_pdf = fitz.open()  # 最终合并的PDF

    for child_pdf in pdfs_path:
        pdf = fitz.open(child_pdf)
        for page_num in range(pdf.page_count):
            merged_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num, start_at=merged_pdf.page_count)
        pdf.close()

    dirpath = os.path.dirname(pdfs_path[0])
    merged_pdf.save(f'{dirpath}/{output}')
    print(f'完成合并：{f'{dirpath}/{output}'}')
    merged_pdf.close()


def split_pdf(pdf_path: str):
    """拆分PDF的每页为单独的PDF"""
    print(f'拆分：{pdf_path}')
    source_pdf = fitz.open(pdf_path)

    page_count = source_pdf.page_count
    if page_count == 1:
        return
    elif page_count > 1:
        filetitle = os.path.basename(os.path.splitext(pdf_path)[0])
        dirpath = os.path.dirname(pdf_path)
        os.mkdir(f'{dirpath}/{filetitle}')
        for page_num in range(source_pdf.page_count):
            single_pdf = fitz.open()
            single_pdf.insert_pdf(source_pdf, from_page=page_num, to_page=page_num)
            single_pdf.save(f'{dirpath}/{filetitle}/{page_num + 1}.pdf')
            single_pdf.close()
        print(f'完成拆分：{f'{dirpath}/{filetitle}'}')

    source_pdf.close()


def get_files(folder: str):
    """获取文件夹下所有文件路径"""
    _files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for j in filenames:
            filepath_join = os.path.normpath(os.path.join(dirpath, j))
            _files.append(filepath_join)

    return _files


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

        # 提取PDF文件路径
        pdfs = [i for i in files if is_pdf(i)]
        if len(pdfs) == 1:  # 执行拆分PDF操作
            split_pdf(pdfs[0])
        elif len(pdfs) > 1:  # 执行合并PDF操作
            merge_pdfs(pdfs)

        print('-' * 20)
        input("\n完成！输入回车后退出...")
    else:
        print("请将文件拖入可执行文件！不支持直接打开使用")
        input("\n输入回车后退出...")
