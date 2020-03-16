import requests
import re
import json


def fetch_url(url):
    try:
        content = requests.get(url).content.decode("gbk")
    except UnicodeDecodeError:
        content = requests.get(url).content.decode("utf-8")
    return content


# 旧版doc文档
def old_doc(content):
    url_list = re.findall(r'(https.*?0.json.*?)\\x22}', content)        # 提取文章所有页链接
    url_list = [addr.replace("\\\\\\/", "/") for addr in url_list]      # 删掉转义字符
    result = []
    for url in url_list[:int(len(url_list)/2)]:                         # 提取的链接只需要用前一半
        content = fetch_url(url)
        temp = ""
        y = 0
        txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),', content)
        for item in txtlists:
            if not y == item[1]:
                y = item[1]
                n = '\n'
            else:
                n = ''
            temp += n
            temp += item[0].encode('utf-8').decode('unicode_escape', 'ignore')
        result.append(temp)
    return result


# 旧版txt文档
def old_txt(content):
    pass


# 新版doc文档
def new_doc(content):
    url_list = re.findall(r'(https:\\\\/\\\\/wkbjcloudbos.*?0.json.*?)\\', content)  # 提取文章所有页链接
    url_list = [addr.replace(r"\\", "") for addr in url_list]                        # 删掉转义字符
    result = []
    for url in url_list[:int(len(url_list))]:                                        # 此版本文库没有多余链接
        content = fetch_url(url)
        temp = ""
        txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),', content)
        y = 0
        for item in txtlists:
            if not y == item[1]:
                y = item[1]
                n = '\n'
            else:
                n = ''
            temp += n
            temp += item[0].encode('utf-8').decode('unicode_escape', 'ignore')
        result.append(temp)
    return result


# 新版txt文档
def new_txt(content):
    txtId = re.findall("show_doc_id\":\"(.*?)\"", content)[0]      # 获取文档id
    md5 = re.findall("md5sum=(.*?)&", content)[0]                   # 获取md5sum值
    sign = re.findall("sign=(.*?)\"", content)[0]                   # 获取sign值
    pageNum = re.findall("\"page\":\"(.*?)\"", content)[0]          # 获取文档总页码数
    resign = re.findall("\"rsign\":\"(.*?)\"", content)[0]          # 获取resign值
    url = "https://wkretype.bdimg.com/retype/text/" + txtId + "?md5sum=" + md5 + "&sign=" + sign + "&callback=cb&pn=1&rn=" + pageNum +\
        "&type=txt&rsign=" + resign                                 # 拼接字符串获取文档链接
    print(url)
    # text = requests.get(url).content.decode('gbk')
    txtcontent = json.loads(fetch_url(url)[3:-1])               # 加载json格式文档
    result = []
    for item in txtcontent:
        temp = ""
        for i in item['parags']:
            temp += i['c'].replace('\\r', '\r').replace('\\n', '\n')
        result.append(temp)
    return result