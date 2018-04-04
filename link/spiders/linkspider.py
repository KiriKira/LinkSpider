import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import IndexItem, DetailItem
from bs4 import BeautifulSoup as bs
import re


class LinkSpider(CrawlSpider):
    name = "link"
    allowed_domains = ["s.lenglianmajia.com", "goods.lenglianmajia.com"]
    start_urls = ["http://s.lenglianmajia.com/list-goodsLine-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-1-1-0-"
                  + str(i) + ".html" for i in range(1, 100)]

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
        item['pinlei'], item['mingchen'], item['leixing'], item['yaoqiu'], item['guige'], item['chechang'], item['chexing'], item['yunfei'], tail1, tail2 = \
            map(lambda i: i.string, block1)

        block2 = soup.find_all('ul')[1].find_all('span')
        item['chufa'], item['mudi'], item['zhuangche'], item['daohuo'] = \
            map(lambda i: i.string, block2)

        item['tag'] = re.match(r"http://goods.lenglianmajia.com/(?P<tag>.*?).shtml", response.url).group("tag")

        return item




