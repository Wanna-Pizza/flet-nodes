import json
import requests

from bs4 import BeautifulSoup

class parser_site:
    def __init__(self) -> None:
        super().__init__()
        self.base_url = "https://www.screenskinz.com"
        self.pages = []
        self.titles = []
        self.find_pages()
        self.find_all() 

    

    def find_pages(self):
        url = self.base_url+'/collections/all'
        responce = requests.get(url)
        soup = BeautifulSoup(responce.text,'html.parser')
        elements = soup.find_all(name='li',class_='collection__nav-links-item')
        for li in elements:
            link = li.find('a')
            if link:
                href = link['href']
                i = 0
                while True:
                    i = i + 1
                    print(i)
                    url_ = self.base_url+href+f'?page={i}'
                    responce = requests.get(url_)
                    soup = BeautifulSoup(responce.text,'html.parser')

                    elements = soup.find_all(name='h6',class_='card-product__title')
                    if elements:
                        self.pages.append(url_)
                    else:
                        break


    def find_titles(self,page_url):

        responce = requests.get(page_url)
        soup = BeautifulSoup(responce.text,'html.parser')

        elements = soup.find_all(name='h6',class_='card-product__title')


        titles = [element.text.strip() for element in elements]
        for title in titles:
            self.titles.append(title)
    
    def find_all(self):
        
        for page_url in self.pages:
            self.find_titles(page_url=page_url)
        print(self.titles)
        print(len(self.titles))
        print(self.pages)
        with open('data_pretty.json', 'w') as json_file:
            json.dump(self.titles, json_file, indent=4)
            
parser_site()



