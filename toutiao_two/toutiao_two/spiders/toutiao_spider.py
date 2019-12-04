# -*- coding: utf-8 -*-
import scrapy
import json
import time
import hashlib
import random
import requests
from datetime import datetime
from ..emailsend import EmailSend
from toutiao_two.items import ToutiaoTwoItem


class ToutiaoSpiderSpider(scrapy.Spider):
    name = 'toutiao_spider'
    allowed_domains = ['www.toutiao.com']
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
        'Host': 'www.toutiao.com',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    cookies = {'tt_webid': '6722356446824613389'}
    start_url = 'https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time='

    max_behot_time = '0'
    D = {'hot_time': '0'}

    def get_as_cp(self):  # 该函数主要是为了获取as和cp参数，程序参考今日头条中的加密js文件：home_4abea46.js
        zz = {}
        now = round(time.time())
        print(now)  # 获取当前计算机时间
        e = hex(int(now)).upper()[2:]  # hex()转换一个整数对象为16进制的字符串表示
        print('e:', e)
        a = hashlib.md5()  # hashlib.md5().hexdigest()创建hash对象并返回16进制结果
        print('a:', a)
        a.update(str(int(now)).encode('utf-8'))
        i = a.hexdigest().upper()
        print('i:', i)
        if len(e) != 8:
            zz = {'as': '479BB4B7254C150',
                  'cp': '7E0AC8874BB0985'}
            return zz

        n = i[:5]
        a = i[-5:]
        r = ''
        s = ''
        for i in range(5):
            s = s + n[i] + e[i]
        for j in range(5):
            r = r + e[j + 3] + a[j]
        zz = {
            'as': 'A1' + s + e[-3:],
            'cp': e[0:3] + r + 'E1'
        }
        print('zz:', zz)
        return zz

    def start_requests(self):
        ascp = self.get_as_cp()
        yield scrapy.FormRequest(url=self.start_url + self.max_behot_time + '&max_behot_time_tmp=' + self.max_behot_time + '&tadrequire=true&as=' + ascp[
                'as'] + '&cp=' + ascp['cp'],
                                 method='GET',
                                 headers=self.headers,
                                 cookies=self.cookies,
                                 callback=self.parse,
                                 )

    def parse(self, response):
        json_result = json.loads(response.text)
        # if json_result is None:
        #     print(self.D['hot_time'], '=====')
        #     time.sleep(20)
        #     yield scrapy.FormRequest(
        #         url=self.start_url + self.D['hot_time'] + '&max_behot_time_tmp=' + self.D['hot_time'] + '&tadrequire=true&as=' +
        #             'A115DD5DE72AC29' + '&cp=' + '5DD7FA9C02D90E1',
        #         method='GET',
        #         headers=self.headers,
        #         cookies=self.cookies,
        #         callback=self.parse,
        #     )
        item = ToutiaoTwoItem()

        infos = json_result['data']
        for info in infos:
            image_url_list = []
            item['abstract'] = info['abstract'] if info.get('abstract') else ''
            item['chinese_tag'] = info['chinese_tag'] if info.get('chinese_tag') else ''
            item['title'] = info['title'] if info.get('title') else ''
            item['source'] = info['source'] if info.get('source') else ''
            image_urls = info['image_list'] if info.get('image_list') else ''
            for image_url in image_urls:
                url = 'https:' + image_url['url']
                image_url_list.append(url)
            item['image_url'] = image_url_list
            yield item
        time.sleep(random.randint(1, 4))
        print(self.D['hot_time'])
        if json_result.get('next'):
            next = json_result['next']
            if next.get('max_behot_time'):
                max_behot_time = str(json_result['next']['max_behot_time'])
                self.D.update({'hot_time': max_behot_time})
                ascp = self.get_as_cp()
                yield scrapy.FormRequest(
                    url=self.start_url + max_behot_time + '&max_behot_time_tmp=' + max_behot_time + '&tadrequire=true&as=' +
                        str(ascp['as']) + '&cp=' + str(ascp['cp']),
                    method='GET',
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.parse,
                    )

    def closed(self, reason):
        # 爬虫关闭的时候，会调用这个方法
        email = EmailSend()
        close_time = 'toutiao爬虫结束时间:{}'.format(datetime.now())
        content = '爬虫关闭原因:{}'.format(reason)
        email.send_text_email('1292770412@qq.com', '1292770412@qq.com', close_time, content)
