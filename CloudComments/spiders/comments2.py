from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import time
import pymysql
from pymongo import MongoClient

# 爬取最大页数
MAX_PAGE = 177
# 歌曲或者MV的ID
ID = 1359811313
# mv or song
CATE = 'song'

browser = webdriver.Chrome()
# 设置等待
wait =  WebDriverWait(browser,10)

url = 'https://music.163.com/{}?id={}'.format(CATE,ID)
browser.get(url)
# 等待框架加载完成
wait.until(EC.presence_of_element_located((By.ID,'g_iframe')))
# 切换框架
browser.switch_to_frame('contentFrame')

def index_page(maxpage):
    for i in range(maxpage):
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.cmmts .itm')))
            get_comments()
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.znxt')))
            button.click()
        except TimeoutException:
            print('请求超时')

def get_comments():
    html = browser.page_source
    doc = pq(html)
    items = doc('.cmmts .itm').items()
    for div in items:
        item = {}
        item['user'] = div.find('.s-fc7').text()
        comment = div.find('.cnt').text()
        item['comment'] = ''.join(comment.split()).lstrip(item['user'])
        item['id'] = int(div.attr('data-id'))
        item['time'] = div.find('.time').text()
        item['like'] = div.find('.zan').parent().text()
        print(item)
        save_to_mongo(item)


def save_to_mongo(item):
    client = MongoClient()
    collection = client['text']['comments2']
    collection.insert(item)


def main():
    index_page(MAX_PAGE)

if __name__ == '__main__':
    main()



