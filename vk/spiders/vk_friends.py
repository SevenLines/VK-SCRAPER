# -*- coding: utf-8 -*-
import json

import scrapy


class VkFriendsSpider(scrapy.Spider):
    name = 'vk_friends'
    allowed_domains = ['vk.com']
    start_urls = ['http://vk.com/']

    def get_url(self, id):
        return 'https://api.vk.com/method/friends.get' \
               '?user_id={id}&v=5.52&count=10000&fields=nickname,bdate,photo_200,education,city,sex'.format(id=id)

    def start_requests(self):
        urls = [("https://api.vk.com/method/users.get" \
                 "?user_id={id}&v=5.52&fields=nickname,bdate,photo_200,education,city,sex".format(id=_id),
                 _id) for _id in self.crawler.settings.get('START_IDS')]

        for url, _id in urls:
            yield scrapy.Request(url, callback=self.parse, meta={
                'user_id': _id,
                'depth': 1,
                'proxy': self.crawler.settings.get('PROXY_URL')
            }, cookies={'remixlang': 0})

    def parse(self, response):
        data = json.loads(response.text)
        items = data['response']['items'] if 'items' in data['response'] else data['response']
        for item in items:
            item['depth'] = response.meta['depth']
            if 'parent_id' in response.meta:
                item['parent_id'] = response.meta['parent_id']
            yield item

            url = self.get_url(item['id'])

            # контроль глубины
            if response.meta['depth'] < self.crawler.settings.get('DEPTH'):
                yield scrapy.Request(url, callback=self.parse, meta={
                    'parent_id': item['id'],
                    'depth': response.meta['depth'] + 1,
                    'proxy': self.crawler.settings.get('PROXY_URL')
                }, cookies={'remixlang': 0})
