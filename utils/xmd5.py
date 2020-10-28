import hashlib


# 获取文件md5
def get_file_md5(file):
    # 将文件指针归零
    file.seek(0)
    myhash = hashlib.md5()
    while True:
        b = file.read(8096)
        if not b:
            break
        # update方法接收bytes，如果读取到的是str，就将str转成bytes
        if isinstance(b, str):
            b = b.encode()
        myhash.update(b)
    return myhash.hexdigest()


if __name__ == '__main__':
    with open('test1.txt') as file1:
        print(get_file_md5(file1))
    with open('test2.txt') as file1:
        print(get_file_md5(file1))
