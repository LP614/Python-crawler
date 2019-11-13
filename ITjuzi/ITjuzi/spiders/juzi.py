# -*- coding: utf-8 -*-
import scrapy
import json
import time
import random
from ITjuzi.items import ItjuziItem
from ITjuzi.settings import USER_AGENT_LIST


class JuziSpider(scrapy.Spider):
    name = 'juzi'
    allowed_domains = ['itjuzi.com']

    def start_requests(self):
        """
        模拟POST请求登录IT桔子网

        """
        header = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Host": "www.itjuzi.com",
            "Referer": "https: // www.itjuzi.com / investevent",
        }
        url = "https://www.itjuzi.com/api/authorizations"
        Payload = {"account": "用户名", "password": "密码", "type": "pswd"}
        yield scrapy.Request(url=url,
                             method="POST",
                             body=json.dumps(Payload),
                             headers=header,
                             callback=self.parse
                             )

    def parse(self, response):
        url = "https://www.itjuzi.com/api/investevents"
        token = json.loads(response.text)['data']['token']
        header = {
            "Content-Type": "application/json",
            "Authorization": token,
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Host": "www.itjuzi.com",
            "Referer": "https: // www.itjuzi.com / investevent",
        }
        payload = {
                    "pagetotal": 0, "total": 0, "per_page": 20, "page": 1, "type": 1, "scope": "", "sub_scope": "",
                    "round": [], "valuation": [], "valuations": "", "ipo_platform": "", "equity_ratio": [""],
                    "status": "", "prov": "", "city": [], "time": [], "selected": "", "location": "", "currency": [],
                    "keyword": ""
                }
        yield scrapy.Request(url=url,
                             method="POST",
                             body=json.dumps(payload),
                             meta={'token': token},
                             headers=header,
                             callback=self.parse_info
                             )

    # 通过计算页数，获取总的页面数，抓取所有数据。
    def parse_info(self, response):
        # 获取传入过来的token
        token = response.meta["token"]
        data = json.loads(response.text)
        # 总数据
        total_number = data['data']['page']['total']
        # 总的页数
        if type(int(total_number) / 20) is not int:
            page = int(int(total_number) / 20) + 1
        else:
            page = int(total_number) / 20
        url = "https://www.itjuzi.com/api/investevents"
        header = {
            "Content-Type": "application/json",
            "Authorization": token,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Host": "www.itjuzi.com",
            "Referer": "https: // www.itjuzi.com / investevent",
        }
        for i in range(1, page):
            time.sleep(1)
            payload = {
                "pagetotal": 0, "total": 0, "per_page": 20, "page": i, "type": 1, "scope": "", "sub_scope": "",
                "round": [], "valuation": [], "valuations": "", "ipo_platform": "", "equity_ratio": [""],
                "status": "", "prov": "", "city": [], "time": [], "selected": "", "location": "", "currency": [],
                "keyword": ""
            }
            # request()中加入dont_filter=True 解决scrapy自身是默认有过滤重复请求的bug。
            # 由于parse_info()函数中 请求的url和parse_detail()函数中请求的URL相同，需要加入dont_filter=True
            yield scrapy.Request(dont_filter=True,
                                 url=url,
                                 method="POST",
                                 body=json.dumps(payload),
                                 headers=header,
                                 callback=self.parse_detail
                                 )

    def parse_detail(self, response):
        infos = json.loads(response.text)["data"]["data"]
        for info in infos:
            item = ItjuziItem()
            item["id"] = info["id"] if info.get('id') else '',
            item["com_id"] = info["com_id"] if info.get('com_id') else '',
            item["name"] = info["name"] if info.get('name') else '',
            item["com_scope"] = info["com_scope"] if info.get('com_scope') else '',
            item["money"] = info["money"] if info.get('money') else '',
            item["money_num"] = info["money_num"] if info.get('money_num') else '',
            item["valuation"] = info["valuation"] if info.get('valuation') else '',
            item["city"] = info["city"] if info.get('city') else '',
            item["agg_time"] = info["agg_time"] if info.get('agg_time') else '',
            item["invse_des"] = info["invse_des"] if info.get('invse_des') else '',
            yield item





