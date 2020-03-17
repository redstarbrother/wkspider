# ********************************使用手册************************************
# *******version列表 通过两个整数判断所爬文章的版本*****************************
# *******第一位 0：旧版文库 1：新版文库****************************************
# *******第二位 1：doc      2：txt       3：pdf          4：ppt **************
# ***************************************************************************
import requests
import re
from gettingdata import *

version = [0, ""]   # 设置版本变量


# request请求函数，返回网页源码
def fetch_url(url):
    global version
    try:
        content = requests.get(url).content.decode("gbk")
    except UnicodeDecodeError:                              # 捕获编码异常，如果有异常说明为新版本页面，用utf-8格式解码
        content = requests.get(url).content.decode("utf-8")
        version[0] = 1
    return content


# 判断文档类型
def verjud(content):
    if version[0] == 0:
        version[1] = re.findall(r"docType.*?\:.*?\'(.*?)\'\,", content)[0]      # 通过正则获取文档类型
        print(version[1])
        # print(type(version[1]))
    else:
        if "indexXreader" in content:
            version[1] = "doc"
        elif "indexTxt" in content:
            version[1] = "txt"
        # print(version[1])



def getarticle(url):
    # url = "https://wenku.baidu.com/view/dbc53006302b3169a45177232f60ddccda38e63d.html?rec_flag=default&sxts=1584344873233" # 旧版doc
    # url = "https://wenku.baidu.com/view/62906818227916888486d74f.html?rec_flag=default"                                     # 新版doc
    # url = "https://wenku.baidu.com/view/ccfb5a96ba68a98271fe910ef12d2af90242a8f5.html?from=search"                          # 新版txt
    # url = input('请输入要下载的文库URL地址')
    # return ["123", "456"]
    content = fetch_url(url)
    verjud(content)
    message = []
    if version[0] == 0:
        if version[1] == "doc":
            message = old_doc(content)
        elif version[1] == "txt":
            message = old_txt(content)
        else:
            pass
    else:
        if version[1] == "doc":
            message = new_doc(content)
        elif version[1] == "txt":
            message = new_txt(content)
        else:
            pass
    # for item in message:
    #     print(item)
    #     print("*"*50)
    return message
