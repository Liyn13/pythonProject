import requests
import re
from bs4 import BeautifulSoup
from time import sleep
from openpyxl import Workbook
from 读取网址 import Homeprice

n = 1
url_list = []
data_list = []

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'}

def get_selling(url):
    response = requests.get(url, headers=headers).text
    selling = re.findall('<a class="a_navnew" hidefocus="true" href="(.*?)" _soj="navigation">新 房</a>', response)

    try:
        return selling[0]
    except IndexError as error:
        pass

def get_details(url):
    response = requests.get(url,headers=headers).text
    detail_url = re.findall('<a class="lp-name" href="(.*?)" soj=".*?"  target="_blank">',response)

    return detail_url

def all_city(all_url):
    response = requests.get(all_url,headers=headers).text
    bsObj = BeautifulSoup(response,'html.parser')
    content = bsObj.find('div', class_='city-itm')

    all = re.findall('<a href="(.*?)">.*?</a>', str(content))
    all = list(set(all))

    for u in all:
        selling_url = get_selling(u)
        if selling_url != None:
            res = requests.get(selling_url,headers=headers).text
            bsObj_1 = BeautifulSoup(res,'html.parser')
            con = bsObj_1.find('div',class_='pagination')
            page_list = re.findall('href="(.*?)"',str(con))
            # print(page_list)

            detail_url = get_details(selling_url)

            for i in detail_url:
                print(i)
                url_list.append(i)

            if page_list:
                for page_url in page_list:
                    for i in get_details(page_url):
                        print(i)
                        url_list.append(i)


    data_list.append((name,price,str(location).strip()))

if __name__ == '__main__':
    all_city('https://www.anjuke.com/sy-city.html')
    aman = Homeprice(url_list)

    book = Workbook()
    sheet = book.active

    for u in url_list:
        try:
            data = aman.get_content(u)
            data_list.append(data)
        except Exception as error:
            with open('error_log.txt','w') as f:
                f.write(error+'\n')
            continue

    for name,price,location in data_list:
        sheet['A' + str(n)] = name
        sheet['B' + str(n)] = price
        sheet['C' + str(n)] = location

        n += 1
    book.save('全国房价.xlsx')