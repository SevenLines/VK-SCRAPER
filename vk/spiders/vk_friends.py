# -*- coding: utf-8 -*-
import json

import scrapy


class VkFriendsSpider(scrapy.Spider):
    name = 'vk_friends'
    allowed_domains = ['vk.com']
    start_urls = ['http://vk.com/']

    def get_url(self, id):
        return 'https://api.vk.com/method/friends.get' \
               '?user_id={id}&v=5.52&fields=nickname,bdate,photo_200,education,city,sex'.format(id=id)

    def start_requests(self):
        urls = [("https://api.vk.com/method/users.get" \
                 "?user_id={id}&v=5.52&fields=nickname,bdate,photo_200,education,city,sex".format(id=_id),
                 _id) for _id in self.crawler.settings.get('START_IDS')]

        for url, _id in urls:
            yield scrapy.Request(url, callback=self.start_parse, meta={
                'user_id': _id,
                'proxy': self.crawler.settings.get('PROXY_URL')
            }, cookies={'remixlang': 0})

    def start_parse(self, response):
        data = json.loads(response.text)
        for item in data['response']:
            item['depth'] = 1
            yield item
        url = self.get_url(item['id'])

        yield scrapy.Request(url, callback=self.parse, meta={
            'parent_id': item['id'],
            'proxy': self.crawler.settings.get('PROXY_URL')
        }, cookies={'remixlang': 0})

    def _parse(self, response, callback):
        data = json.loads(response.text)
        for item in data['response']['items']:
            item['depth'] = 2
            item['parent_id'] = response.meta['parent_id']
            yield item

            # url = self.get_url(item['id'])
            # yield scrapy.Request(url, callback=callback, meta={
            #     'parent_id': item['id'],
            #     'proxy': self.crawler.settings.get('PROXY_URL')
            # }, cookies={'remixlang': 0})

    def parse(self, response):
        return self._parse(response, self.parse2)

    def parse2(self, response):
        data = json.loads(response.text)
        for item in data['response']['items']:
            item['depth'] = 3
            item['parent_id'] = response.meta['parent_id']
            yield item
