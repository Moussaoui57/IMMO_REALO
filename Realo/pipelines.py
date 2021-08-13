# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from csv import QUOTE_ALL
import datetime
from scrapy.utils.project import get_project_settings
import socket
import logging
from twisted.python.failure import Failure
from scrapy.utils.request import referer_str
import time
import pprint
from scrapy import signals
from scrapy.exporters import CsvItemExporter



class RealoPipeline:

    def __init__(self):
        self.files = {}


    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline


    def spider_opened(self, spider):
        file = open('%s.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file, delimiter=';', quotechar='"', quoting=QUOTE_ALL)
        self.exporter.start_exporting()
        self.exporter.fields_to_export = ["ANNONCE_LINK","FROM_SITE","ID_CLIENT","ANNONCE_DATE","ACHAT_LOC","SOLD","MAISON_APT","CATEGORIE","NEUF_IND","NOM","ADRESSE","CP","VILLE","QUARTIER","DEPARTEMENT","REGION","PROVINCE","ANNONCE_TEXT","ETAGE","NB_ETAGE","LATITUDE","LONGITUDE","M2_TOTALE","SURFACE_TERRAIN","NB_GARAGE","PHOTO","PIECE","PRIX","PRIX_M2","URL_PROMO","STOCK_NEUF","PAYS_AD","PRO_IND","SELLER_TYPE","MINI_SITE_URL","MINI_SITE_ID","AGENCE_NOM","AGENCE_ADRESSE","AGENCE_CP","AGENCE_VILLE","AGENCE_DEPARTEMENT","EMAIL","WEBSITE","AGENCE_TEL","AGENCE_TEL_2","AGENCE_TEL_3","AGENCE_TEL_4","AGENCE_FAX","AGENCE_CONTACT","PAYS_DEALER","FLUX","SITE_SOCIETE_URL","SITE_SOCIETE_ID","SITE_SOCIETE_NAME","AGENCE_RCS","SPIR_ID","vat_number","ipi_number","ANNONCEUR"]

    def spider_closed(self, spider,reason):
        return 'finished'





    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item




