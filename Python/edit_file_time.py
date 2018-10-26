# modified from '如何用python批量修改文件创建时间？ - 嫖鸡大将军的回答 - 知乎'https://www.zhihu.com/question/38430949/answer/365225880

from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle, GetFileAttributes
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
import time
import random

import sys
import os

if len(sys.argv) < 5:
    pfile = os.path.basename(sys.argv[0])
    print("USAGE:\n\t%s <createTime> <modifyTime> <accessTime> <FileName>\n" % pfile)
    print("EXAMPLE:")
    print('%s "01.01.2000 00:00:00" "01.01.2000 00:00:00" "01.01.2000 00:00:00" file' % (pfile))
    # sys.exit()

# get arguments
# cTime = sys.argv[1] # create
# mTime = sys.argv[2] # modify
# aTime = sys.argv[3] # access
# fName = sys.argv[4]



def get_file_name_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list, key=lambda x: os.path.getctime(os.path.join(file_path, x)))
        # print(dir_list)
        return dir_list



def edit_file_list_time(c_time, dir_path, file_name_list):
    # get arguments
    # c_time = "08.10.2018 15:34:44"
    m_time = c_time
    a_time = c_time

    time_format = "%d.%m.%Y %H:%M:%S"
    c_time_stripe = time.strptime(c_time, time_format)
    m_time_stripe = time.strptime(m_time, time_format)
    a_time_stripe = time.strptime(a_time, time_format)

    c_time_second = time.mktime(c_time_stripe)
    m_time_second = time.mktime(m_time_stripe)
    a_time_second = time.mktime(a_time_stripe)

    for fileName in file_name_list:
        # f_name = "h:\Downloads\待处理文件\20180702.xls"
        f_name = dir_path + fileName
        # specify time format
        offset = random.randint(60, 150)  # in seconds

        # create struct_time object
        c_time_second = c_time_second + offset
        m_time_second = m_time_second + offset
        a_time_second = a_time_second + offset

        c_time_t = time.localtime(c_time_second)
        m_time_t = time.localtime(m_time_second)
        a_time_t = time.localtime(a_time_second)

        # visually check if conversion was ok
        print()
        print("FileName: %s" % f_name)
        print("Create  : %s --> %s OK" % (c_time, time.strftime(time_format, c_time_t)))
        print("Modify  : %s --> %s OK" % (m_time, time.strftime(time_format, m_time_t)))
        print("Access  : %s --> %s OK" % (a_time, time.strftime(time_format, a_time_t)))
        print()

        # change timestamp of file
        fh = CreateFile(f_name, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        create_time, access_time, modify_time = GetFileTime(fh)
        print("Change Create from", create_time, "to %s" % (time.strftime(time_format, c_time_t)))
        print("Change Modify from", modify_time, "to %s" % (time.strftime(time_format, m_time_t)))
        print("Change Access from", access_time, "to %s" % (time.strftime(time_format, a_time_t)))
        print()

        create_time = Time(time.mktime(c_time_t))
        access_time = Time(time.mktime(a_time_t))
        modify_time = Time(time.mktime(m_time_t))
        SetFileTime(fh, create_time, access_time, modify_time)
        CloseHandle(fh)

        # check if all was ok
        ctime = time.strftime(time_format, time.localtime(os.path.getctime(f_name)))
        mtime = time.strftime(time_format, time.localtime(os.path.getmtime(f_name)))
        atime = time.strftime(time_format, time.localtime(os.path.getatime(f_name)))

        print("CHECK MODIFICATION:")
        print("FileName: %s" % f_name)
        print("Create  : %s" % ctime)
        print("Modify  : %s" % mtime)
        print("Access  : %s" % atime)

'''
增加起、止时间、时间间隔设置
'''
def edit_file_list_time(start_time,end_time,lapse, dir_path, file_name_list):
    # get arguments
    c_time = start_time
    m_time = c_time
    a_time = c_time

    time_format = "%d.%m.%Y %H:%M:%S"
    start_time_stripe = time.strptime(start_time, time_format)
    end_time_stripe = time.strptime(end_time, time_format)
    c_time_stripe = time.strptime(c_time, time_format)
    m_time_stripe = time.strptime(m_time, time_format)
    a_time_stripe = time.strptime(a_time, time_format)

    start_time_second = time.mktime(start_time_stripe)
    end_time_second = time.mktime(end_time_stripe)
    c_time_second = time.mktime(c_time_stripe)
    m_time_second = time.mktime(m_time_stripe)
    a_time_second = time.mktime(a_time_stripe)

    size = len(file_name_list)

    if lapse==None:
        lapse = int((end_time_second-start_time_second)/size)

    for fileName in file_name_list:
        # f_name = "h:\Downloads\待处理文件\20180702.xls"
        f_name = dir_path + fileName
        # specify time format
        offset = random.randint(int(lapse-lapse/10), int(lapse+lapse/10))  # in seconds

        # create struct_time object
        c_time_second = c_time_second + offset
        m_time_second = m_time_second + offset
        a_time_second = a_time_second + offset

        c_time_t = time.localtime(c_time_second)
        m_time_t = time.localtime(m_time_second)
        a_time_t = time.localtime(a_time_second)

        # visually check if conversion was ok
        print()
        print("FileName: %s" % f_name)
        print("Create  : %s --> %s OK" % (c_time, time.strftime(time_format, c_time_t)))
        print("Modify  : %s --> %s OK" % (m_time, time.strftime(time_format, m_time_t)))
        print("Access  : %s --> %s OK" % (a_time, time.strftime(time_format, a_time_t)))
        print()

        # change timestamp of file
        fh = CreateFile(f_name, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        create_time, access_time, modify_time = GetFileTime(fh)
        print("Change Create from", create_time, "to %s" % (time.strftime(time_format, c_time_t)))
        print("Change Modify from", modify_time, "to %s" % (time.strftime(time_format, m_time_t)))
        print("Change Access from", access_time, "to %s" % (time.strftime(time_format, a_time_t)))
        print()

        create_time = Time(time.mktime(c_time_t))
        access_time = Time(time.mktime(a_time_t))
        modify_time = Time(time.mktime(m_time_t))
        SetFileTime(fh, create_time, access_time, modify_time)
        CloseHandle(fh)

        # check if all was ok
        ctime = time.strftime(time_format, time.localtime(os.path.getctime(f_name)))
        mtime = time.strftime(time_format, time.localtime(os.path.getmtime(f_name)))
        atime = time.strftime(time_format, time.localtime(os.path.getatime(f_name)))

        print("CHECK MODIFICATION:")
        print("FileName: %s" % f_name)
        print("Create  : %s" % ctime)
        print("Modify  : %s" % mtime)
        print("Access  : %s" % atime)

if __name__=='__main__':
    DIR = "h:\Downloads\待处理文件/"

    # fileNameList = get_file_name_list(DIR)
    # for file in fileNameList:
    # 验证顺序是否正确
    #   print(file)

    edit_file_list_time("08.10.2018 15:34:44", DIR, fileNameList)
