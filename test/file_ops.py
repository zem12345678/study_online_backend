import os
from utils.xmd5 import get_file_md5


# 测试文件分块
def test_chunk():
    src_file = open('lucene.avi', 'rb')
    chunk_path = 'chunk/'
    chunk_size = 1024 * 1024
    counter = 1
    # 检查chunk_path是否存在，如不存在则创建
    if not os.path.exists(chunk_path):
        os.makedirs(chunk_path)
    while True:
        # 1、循环从文件中读取指定大小的内容
        chunk_content = src_file.read(chunk_size)
        # 2、如果不能读取到内容，则退出循环
        if not chunk_content:
            break
        # 3、如果能读取到内容，则将其写入到chunk目录下
        with open(chunk_path+str(counter), 'wb') as f:
            f.write(chunk_content)
        counter += 1
    print(get_file_md5(src_file))
    src_file.close()


# 测试文件合并
def test_merge():
    chunk_path = 'chunk/'
    # 1、找到分块文件并按文件名进行排序。
    _, _, files = next(os.walk(chunk_path))
    files.sort(key=lambda name: int(name))
    merge_file_path = 'lucene.avi'
    # 检查文件是否存在，如果存在则先删除
    if os.path.exists(merge_file_path):
        os.remove(merge_file_path)
    # 2、创建合并文件
    merge_file = open(merge_file_path, 'wb+')
    # 3、依次从分块文件中读取数据并向合并文件写入
    for file_name in files:
        with open(chunk_path+file_name, 'rb') as chunk_file:
            merge_file.write(chunk_file.read())
    print(get_file_md5(merge_file))
    merge_file.close()


if __name__ == '__main__':
    # test_chunk()    # c5c75d70f382e6016d2f506d134eee11
    test_merge()    # c5c75d70f382e6016d2f506d134eee11
