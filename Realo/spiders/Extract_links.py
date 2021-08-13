# -*- coding: utf-8 -*-
import scrapy 
import re 
from scrapy.http import Request, FormRequest
import requests
import json
import pandas as pd
import csv
from pandas.io.json import json_normalize

class SpiderSpider(scrapy.Spider):
    name = 'Realo_05_2021'
    allowed_domains = ['realo.be']
    start_urls = ['https://www.realo.be/sitemap/generated/search.fr.1.xml','https://www.realo.be/sitemap/generated/search.fr.2.xml','https://www.realo.be/sitemap/generated/district.1.xml']
    
    def parse(self,response):
        liste_urls = re.findall("(https[^<>\"]+)", response.text)
        for url in liste_urls:
            lien = url.replace('\n','').replace('/nl/','')
            yield Request(lien, self.parse_detail)

    def parse_detail(self, response):
        if "Aucun résultat" not in response.text:
            liste = response.xpath('//li[@data-id="componentEstateListGridItem"]')
            for i in liste:
                link = i.xpath('./div/div/a[@class="link"]/@href').extract_first()
                link = "https://www.realo.be" + link.replace('\n','')
                yield scrapy.Request(url=link,callback=self.parse_detail_1)

        next_page =response.xpath('//a[@rel="next"]/@href').extract_first() 
        if next_page:
            next_page = "https://www.realo.be" + next_page
            yield scrapy.Request(url=next_page,callback=self.parse_detail)
    def parse_detail_1(self,response):
        item = {}
        item["ANNONCE_LINK"] = response.url
        #item["ID_CLIENT"] = response.url.split('?l=')[1]
        nom1= response.xpath('//div[@class="type"]/strong/text()').extract_first()
        nom2 = response.xpath('//div[@class="type"]/text()').extract_first()
        try:
            if nom2.replace('\n','').replace('\t','').strip():
                item["NOM"] = nom2.replace('\n','').replace('\t','').strip()
            else:
                item["NOM"] = nom1.replace('\n','').replace('\t','').strip()
        except:
            item["NOM"] = ""
        yield item
