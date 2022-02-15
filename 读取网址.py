import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'}
class Homeprice:
    def __init__(self,url_list):
        self.url_list = url_list

    def get_content(self,url):
        response = requests.get(url,headers=headers).text
        bsObj = BeautifulSoup(response,'html.parser')

        self.name = bsObj.h1.text
        self.location = str(bsObj.find('a', class_='lpAddr-text g-overflow').text).strip()

        try:
            self.price = bsObj.find('em',class_='sp-price other-price').text
        except AttributeError as error:
            self.price = bsObj.find('i',class_='sp-price other-price')

        # print((self.name,self.location,self.price))
        return (self.name,self.location,self.price)