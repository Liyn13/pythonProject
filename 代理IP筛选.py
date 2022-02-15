import re
import os
import requests
from time import sleep
from random import choice
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'}
ip_list = []

def page(url):
    response = requests.get(url,headers=headers).text

    return re.findall('<span title=".*?"> / (\d+) 页</span>',response)[0]

def ip_pool(ip):

    ip_data = {
        'http':'http://'+ip,
        'https':'https://'+ip,
        }

    return ip_data

def save(name,url):

    sleep(1)

    try:
        randomIp = ip_pool(choice(ip_list))
        response = requests.get(url,headers=headers,proxies=randomIp,timeout=8).text
        print(randomIp)
        bsObj = BeautifulSoup(response,'html.parser')
    except Exception as error:
        print(error)
        response = requests.get(url,headers=headers,timeout=8).text
        bsObj = BeautifulSoup(response,'html.parser')

    content = bsObj.find('div',style='padding:15px 0;')
    if content:
        will_save = content.get_text()[19:]
        try:
            path = os.getcwd()+'\吾爱破解python区代码2\\'
            if not os.path.exists(path):
                os.mkdir(path)

            with open(path + name + '.py', 'w', encoding='utf-8') as file:
                file.write(will_save)
        except Exception as error:
            print(error)
    else:
        pass



def main(url):
    response = requests.get(url,headers=headers).text
    bsObj = BeautifulSoup(response, 'html.parser')

    for item in bsObj.find_all('a', class_='s xst'):
        if item:
            pageu = 'https://www.52pojie.cn/'+item['href']
            title = item.get_text()
            print(title,pageu)
            save(title,pageu)

    sleep(1)


all_page = page('https://www.52pojie.cn/forum.php?mod=forumdisplay&fid=24&filter=typeid&typeid=29')

content = open('存活代理列表.txt', 'r')
for item in content.readlines():
    ip_list.append(item.strip())

for page in range(1,int(all_page)+1):
    url = 'https://www.52pojie.cn/forum.php?mod=forumdisplay&fid=24&typeid=29&filter=typeid&typeid=29&page='+str(page)
    print('第%d页，URL：' % page,url)
    main(url)