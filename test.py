import re
import requests

session = requests.session()

def fetch_url(url):
    return requests.get(url)

# content_s = fetch_url('https://wenku.baidu.com/view/6a3902665627a5e9856a561252d380eb6294239f.html?rec_flag=default')
content_s = fetch_url('https://wenku.baidu.com/view/62906818227916888486d74f.html?rec_flag=default')  # new
content_s = content_s.content.decode('gbk')
# url_list = re.findall(r'(https.*?0.json.*?)\\x22', content_s)
kk = re.compile(r'(https:\\\\/\\\\/wkbjcloudbos.*?0.json.*?)\\')
url_list = kk.findall(content_s)
# print(content_s.content)
new_url_list = []
# print(len(url_list))
for temp in url_list:
    temp = temp.replace(r"\\", "")
    print(temp, end='\n')
    new_url_list.append(temp)
result = ""
for url in new_url_list[:int(len(new_url_list))]:
    content = fetch_url(url)
    content = content.content.decode('utf-8')
    txtlists = re.findall('"c":"(.*?)".*?"y":(.*?),', content)

    y = 0
    for item in txtlists:
        if not y == item[1]:
            y = item[1]
            n = '\n'
        else:
            n = ''
        result = item[0].encode('utf-8').decode('unicode_escape', 'ignore')
        print(result)
# content = fetch_url(url)
# print(content)
# print(url)

def get_doc_id(url):
    return re.findall('view/(.*).html', url)[0]


def parse_type(content):
    return re.findall(r"docType.*?\:.*?\'(.*?)\'\,", content)[0]


def parse_title(content):
    return re.findall(r"title.*?\:.*?\'(.*?)\'\,", content)[0]
