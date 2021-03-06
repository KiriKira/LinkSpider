# -*-  coding：utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import IndexItem, DetailItem
from bs4 import BeautifulSoup as bs
import re, json, os
from ..spiders.addresssplit import address_split

with open(os.path.dirname(__file__) + "/" + "shengdata.json", "r") as f:
    shengdata = json.load(f)

with open(os.path.dirname(__file__) + "/" + "shidata.json", "r") as f:
    shidata = json.load(f)
    print(shidata)


class LinkSpider(CrawlSpider):
    name = "link"
    allowed_domains = ["s.lenglianmajia.com", "goods.lenglianmajia.com"]
    start_urls = ["http://s.lenglianmajia.com/list-goodsLine-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-1-1-0-"
                  + str(i) + ".html" for i in range(1, 6)]

    rules = (Rule(LinkExtractor(
        allow=('http://s.lenglianmajia.com/list-goodsLine-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-1-1-0-\d+.html',),
        deny_domains=['misc.lenglianmajia.com', 'login.lenglianmajia.com',
                      'd.lenglianmajia.com', 'www.lenglianmajia.com',
                      'ep.lenglianmajia.com']),
                  follow=True, callback='index_parser'),
             Rule(LinkExtractor(allow=('http://goods.lenglianmajia.com/.*\.shtml',)), callback='detail_parser')
             )

    def index_parser(self, response):
        self.logger.info('this is an index page! %s', response.url)

        soup = bs(response.body.decode('utf-8'), 'html.parser')
        tag_qiangdan = []
        for i in range(1, 10):
            item = soup.find_all('tr')[i]
            onclick = item.get('onclick')
            url = re.match(r".*(?P<url>http://.*shtml).*", onclick).group("url")
            tag = re.match(r"http://goods.lenglianmajia.com/(?P<tag>.*?).shtml", url).group("tag")
            # print(url)
            if item.a.string == '抢单':
                qiangdan = 0
            else:
                qiangdan = 1
            tag_qiangdan.append((tag, qiangdan))

        item = IndexItem()
        item['tag_qiangdan'] = tag_qiangdan

        return item

    def detail_parser(self, response):
        self.logger.info('this is an detail page! %s', response.url)

        soup = bs(response.body.decode('utf-8'), 'html.parser')
        item = DetailItem()

        block1 = soup.ul.find_all('span')
        item['pinlei'], item['mingchen'], item['leixing'], yaoqiu, guige, item['chechang'], item['chexing'],\
            item['yunfei'], tail1, tail2 = \
            map(lambda i: i.string, block1)

        item['guige'] = guige[:-2]

#       spilt yaoqiu to two items
        try:
            item['yaoqiu01'] = yaoqiu.split('~')[0]
            item['yaoqiu02'] = yaoqiu.split('~')[1][:-1]
        except IndexError as e:
            item['yaoqiu01'] = yaoqiu
            item['yaoqiu02'] = 0
        except Exception as e:
            item['yaoqiu01'] = yaoqiu
            item['yaoqiu02'] = str(e)


#       delete "yuan" and ","
        item['yunfei'] = ''.join(item['yunfei'][:-1].split(","))

        block2 = soup.find_all('ul')[1].find_all('span')
        chufa, mudi, zhuangche, daohuo = \
            map(lambda i: i.string, block2)

        item['chufa01'], item['chufa02'], item['chufa03'] = address_split(chufa)
        item['mudi01'], item['mudi02'], item['mudi03'] = address_split(mudi)

        try:
            item['chufa_shengnumber'] = shengdata[item['chufa01']]
        except KeyError:
            item['chufa_shengnumber'] = None

        try:
            item['chufa_shinumber'] = shidata[item['chufa02']]
        except KeyError:
            item['chufa_shinumber'] = None

        try:
            item['mudi_shengnumber'] = shengdata[item['chufa01']]
        except KeyError:
            item['mudi_shengnumber'] = None

        try:
            item['mudi_shinumber'] = shidata[item['chufa02']]
        except KeyError:
            item['mudi_shinumber'] = None

        zhuangche_splite = re.split(r'-|——', zhuangche)
        item['zhuangche01'] = ''.join(zhuangche_splite[:3])
        item['zhuangche02'] = ''.join(zhuangche_splite[3:])

        daohuo_splite = re.split(r'-|——', daohuo)
        item['daohuo01'] = ''.join(daohuo_splite[:3])
        item['daohuo02'] = ''.join(daohuo_splite[3:])

        item['tag'] = re.match(r"http://goods.lenglianmajia.com/(?P<tag>.*?).shtml", response.url).group("tag")

        return item




