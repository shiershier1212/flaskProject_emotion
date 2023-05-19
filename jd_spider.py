# encoding=utf-8
import json
import re
import time

import requests
from bs4 import BeautifulSoup
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76'
}


def spider(product_url):
    pattern = r'https://item.jd.com/(\d+)\.html'
    match = re.search(pattern, product_url)
    product_id = ''  # 获取当前商品的商品id
    if match:
        product_id = match.group(1)
    # print(product_id)

    comment_list = []  # 评论列表，每一项都是一个评论

    with open(f'./spider_data/{product_id}_comments.txt', 'w', encoding='utf-8') as f:
        for i in range(0, 5):
            time.sleep(2.5)
            url = f'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc&clientVersion=1.0.0&t=1684468692049&loginType=3&uuid=122270672.1683459379064608177886.1683459379.1684465032.1684468079.3&productId={product_id}&score=0&sortType=5&page={i}&pageSize=10&isShadowSku=0&rid=0&fold=1&bbtf=1&shield='
            response = requests.get(url=url, headers=headers)
            data_list = json.loads(response.text)['comments']
            for j in range(0, len(data_list)):
                review = data_list[j]['content'].replace('\n', ' ')
                # print()
                comment_list.append(review)
                # f.writelines(review+'\n')

    # page_text = requests.get(url=product_url, headers=headers).text
    # tree = etree.HTML(page_text)
    #
    # r = tree.xpath('//div[@class="sku-name"]/text()')
    # product_name = r[1].replace(' ', '')

    return comment_list


def getProductInfo(product_url):
    pattern = r'https://item.jd.com/(\d+)\.html'
    match = re.search(pattern, product_url)
    product_id = ''  # 获取当前商品的商品id
    if match:
        product_id = match.group(1)

    page_text = requests.get(url=product_url,headers=headers).text
    tree = etree.HTML(page_text)

    r = tree.xpath('//div[@class="sku-name"]/text()')
    product_name = r[1].replace(' ','')

    product_price = tree.xpath(f'//span[@class="price J-p-{product_id}"]/text()')

    # print(page_text)

    pattern2 = fr'<span class="price J-p-{product_id}">(\d+)\</span>'
    print(f'<span class="price J-p-{product_id}">')
    match2 = re.search(pattern2,page_text)
    print(match2)
    print(product_name,product_price)
