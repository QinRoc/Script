'''

Python之修改文件MD5值 https://www.cnblogs.com/huangshiyu13/p/6823537.html
python 计算文件 md5, sha1, crc32 https://mozillazg.wordpress.com/2011/05/20/python-file-hash/
'''

import os

import hashlib
import zlib
import os
from time import localtime, strftime

'''
hash 计算 MD5 、SHA1

提供要计算 hash 值的
- 文件路径
- 文件大小
- 每次读取的文件块大小
- 算法的摘要对象

返回字符串类型的 hash 值
'''
def hash_value(filename, filesize, maxsize, xhash):

    with open(filename, 'rb') as openfile: # 打开文件，一定要是以二进制打开
        while True:
            data = openfile.read(maxsize) # 读取文件块
            if not data: # 直到读完文件
                break
            xhash.update(data)
    return xhash.hexdigest()

def alert_file_md5(filename):
    print(filename + ' md5 is '+hash_value(filename,os.path.getsize(filename),1024 * 1024,hashlib.md5()))
    myfile = open(filename,'a')
    myfile.write("####&&&&")
    myfile.close
    print(filename + ' new md5 is '+hash_value(filename,os.path.getsize(filename),1024 * 1024,hashlib.md5()))

if __name__ == '__main__':
    filename = 'h:\Downloads\Test\2017.04.08.xls'
    alert_file_md5(filename)
    print(filename + ' is Changed.')
