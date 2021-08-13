# -*- coding: utf-8 -*-
import scrapy 
import re 
from scrapy.http import Request, FormRequest

class SpiderSpider(scrapy.Spider):
    name = 'realo_immeuble_2021_05'
    allowed_domains = ['realo.be']
    def start_requests(self):
        f = open('Immeuble.txt', 'r')
        lignes = f.readlines()
        f.close()
        for url in lignes:
            yield Request(url.rstrip('\n\r'), self.parse)
    def parse(self, response):
        liste = response.xpath("//ul[@class='row list-unstyled listings__list']/li")  #response.xpath('//div[@class[contains(.,"multi-unit")]]/div/ul/li')  #response.xpath('//div[@class[contains(.,"multi-unit")]]/ul/li/div/ul/li[@class=""]')
        for i in liste:
            item = {}
            item["URL_PROMO"] = response.url
            item["NEUF_IND"] = 'Y'
            link = i.xpath('./a/@href').extract_first()
            base = "https://www.realo.be"
            lien = base + link
            yield Request(lien, self.parse_detail, meta={'item':item})
    def parse_detail(self, response):
        item = response.meta['item']
        item["ANNONCE_LINK"] = response.url
        item["FROM_SITE"]="REALO"

        try:
            item["NOM"] =response.xpath('//title/text()').extract_first().strip().replace(";","")


        except:
            pass
        try:
            item["ID_CLIENT"] = response.url.split("=")[1].replace("\n","")

        except:
            pass
        
        #try:
        #    item['ANNONCE_DATE']=response.xpath('//div[@class="type"]').get().split("il y a")[-1].replace("\n","").replace("\t","").replace("</div>","").replace("\n","").replace('<div class=""type""><strong>Pas à vendre ni à louer via Realo</strong>','').strip()

        #except:
        #    pass 


        try:
            A=re.findall('data-way="(.*?)"',response.text)[0]

            if A =="RENT":
       	        item["ACHAT_LOC"]="2"
            else:
                item["ACHAT_LOC"]="1"

        except:
            pass


        try:
            all = response.xpath('//script[@data-name="modal_share_listing"]').extract_first().strip()
            categorie =re.findall('....." data-type="(.*?)"',all)[0]
            if categorie == "NEWBUILD_PROJECT":
                item["CATEGORIE"] = ', '.join(set(response.xpath('//ul[@class="row list-unstyled listings__list"]/li/div/div/div/span[@class="type"]/text()').extract())).replace('\n','')
                #item["NEUF_IND"]="Y"
                prix_m = response.xpath('//div[@data-id="componentPropertyFeatures"]/div/table/tbody/tr/td[@class="name"]/text()').extract()
                for prix in prix_m:
                    if "Prix" in prix:
                        ind = prix_m.index(prix)
                        item["PRIX"] = response.xpath('//div[@data-id="componentPropertyFeatures"]/div/table/tbody/tr/td[@class="value"]/text()').extract()[ind+1].split('de')[1].replace('€','').replace('.','').strip()
                for m2 in prix_m:
                    if "Surface" in m2:
                        ind2 = prix_m.index(m2)
                        item["M2_TOTALE"] = response.xpath('//div[@data-id="componentPropertyFeatures"]/div/table/tbody/tr/td[@class="value"]/text()').extract()[ind2+1].split('de')[1].replace('m','').strip()
                item["STOCK_NEUF"]= len(response.xpath('//ul[@class="row list-unstyled listings__list"]/li[@class=""]').extract())
                item['ANNONCE_DATE']= ""
            else:
                item["CATEGORIE"] = categorie
                #item["NEUF_IND"]="N"
                item["M2_TOTALE"]=response.xpath('//td[contains(text(),"Surface habitable")]/../td[2]/text()').extract_first().strip().replace('m','')
                item["PRIX"]=[i for i in response.xpath('//div[@class="value"]/text()').extract() if ' ' in i][0].split(' ')[0].strip().replace('.','').replace("Pas","")
                item["STOCK_NEUF"]=""
                item['ANNONCE_DATE']=response.xpath('//div[@class="type"]').get().split("il y a")[-1].replace("\n","").replace("\t","").replace("</div>","").replace("\n","").replace('<div class=""type""><strong>Pas à vendre ni à louer via Realo</strong>','').strip()
        except:
            pass

        try:
            all = response.xpath('//script[@data-name="modal_share_listing"]').extract_first().strip()
            cat=re.findall('....." data-type="(.*?)"',all)[0]
            if cat=="HOUSE":
                item["MAISON_APT"]="1"
            elif cat=="APARTMENT":
                item["MAISON_APT"]="2"
            elif cat== "BUSINESS":
                item["MAISON_APT"]="5"
            elif cat== "OFFICE":
                item["MAISON_APT"]="19" 
             
            elif cat== "LAND":
                item["MAISON_APT"]="6"
            elif cat== "PARKING":
                item["MAISON_APT"]="4"

            elif cat== "HOLIDAY_RESORT":
                item["MAISON_APT"]="41"
            elif cat== "INDUSTRIAL":
                item["MAISON_APT"]="16"
            elif cat== "INVESTMENT_PROPERTY":
                item["MAISON_APT"]="7"
            elif cat== "MISCELLANEOUS":
                item["MAISON_APT"]="8"
            elif cat== "ROOM":
                item["MAISON_APT"]="3"  
        except:
            pass


        
        # ===> DONE
        ad = response.xpath('//*/@data-address-name').extract_first()
        if ad:
            ad = ad.split('\n')
            if len(ad) == 2:
                item["CP"] = ad[0].split(' ')[0].replace("Nam","")
                item["VILLE"] = ' '.join(ad[0].split(' ')[1:])
                item["ADRESSE"] = ""
            elif len(ad) == 3:
                item["CP"] = ad[1].split(' ')[0].replace("Nam","")
                item["VILLE"] = ' '.join(ad[1].split(' ')[1:])
                item["ADRESSE"] = ad[0]
            elif len(ad) == 1:
                item["CP"] = ""
                item["VILLE"] = ""
                item["ADRESSE"] = ad[0]
        else:
            item["CP"] = ""
            item["VILLE"] = ""
            item["ADRESSE"] = ""
      
        try: 
 
            item["QUARTIER"]=response.xpath('//div[@class="breadcrumb"]/ul/li[4]/a/text()').extract_first().strip()

        except:
            item["QUARTIER"]=""

        try:
            item['PROVINCE']= re.findall('"propertyProvinceDimension":"(.*?)"',response.text)[0].strip().replace('Li\u00e8ge','Liège')

        except:
            pass 

        try:
            item["ANNONCE_TEXT"]=' '.join(response.xpath('//div[@class="component-property-description "]/div/p/text()').extract()).replace('\r','').replace('\n','').replace('\t','').strip().replace(";","")

        except:
            pass

        item["ETAGE"]=""
        item["NB_ETAGE"]=""
        #==> DONE    
        try:
            item["LATITUDE"]=re.findall('data-latlng="(.*]?)',response.text)[0].split(",")[0].replace("[","").replace("\n","").replace('"','').strip()
        except: 
            pass

        try:
            item["LONGITUDE"]=re.findall('data-latlng="(.*]?)',response.text)[0].split(",")[1].replace("]","").replace("\n","").replace('"','').strip()
        except:
            pass
        #==> DONE
        #try:
        #    item["M2_TOTALE"]=response.xpath('//td[contains(text(),"Surface habitable")]/../td[2]/text()').extract_first().strip().replace('m','')
        #except :
        #    pass
        # ==> DONE
        try:
            item["SURFACE_TERRAIN"]= response.xpath('//td[contains(text(),"Superficie de la parcelle")]/../td[2]/text()').extract_first().strip().replace('m','')  
            #' '.join(response.xpath('//div[@class="component-property-features"]//tbody/tr[6]//td/text()').extract()).replace("\t","").replace("\n","").split(" ")[-1].replace('m','')
        except:
            pass
        # ==> DONE
        try:
            item["NB_GARAGE"]=response.xpath('//td[contains(text(),"parking")]/../td[2]/text()').extract_first().strip()
        except:
            pass
          
        try:
            item["PHOTO"]=response.xpath('//a[@class="button-fullscreen"]/text()').extract_first().split(' ')[1].strip()
        except:
            pass
          
        try:

            item["PIECE"]=response.xpath('//td[contains(text(),"Chambres")]/../td[2]/text()').extract_first()  #' '.join(response.xpath('//div[@class="component-property-features"]//tbody/tr[3]//td/text()').extract()).replace("\t","").replace("\n","").split(" ")[-1].replace('m','').replace('Non','').strip()
        except:
            pass
        # ==> DONE
        #try:
 
         #   item["PRIX"]=[i for i in response.xpath('//div[@class="value"]/text()').extract() if ' ' in i][0].split(' ')[0].strip().replace('.','').replace("Pas","")
        #except:
        #    pass


        item["PRIX_M2"]=""


        #item["STOCK_NEUF"]=""
 
        try:
            item["PAYS_AD"]=response.xpath("//div[@class='popover-container hidden']//a/text()").get().replace("\n","")
        except:
            pass

        try:
            item["ANNONCEUR"]=response.xpath('//a[@class="btn btn--md btn--blue"]/text()').extract_first().split("sur")[-1].strip()
        except:
            pass



        #==> DONE
        tel = re.findall('tel:(.*?)"',response.text)
        tel2 = response.xpath('//a[@data-type="phone"]/@data-phone-number').extract_first()
        if tel:
            item["AGENCE_TEL"]= tel[0].strip()
        elif tel2:
            item["AGENCE_TEL"]= tel2
        else:
            item["AGENCE_TEL"]= ""
        item["AGENCE_TEL_2"]=""
        item["AGENCE_TEL_3"]=""
        item["AGENCE_TEL_4"]=""
        item["AGENCE_FAX"]=""
        item["AGENCE_CONTACT"]=""
        item["PAYS_DELER"]=""
        item["FLUX"]=""
        item["SITE_SOCIETE_URL"]=""
        item["SITE_SOCIETE_NAME"]=""
        item["SITE_SOCIETE_ID"]=""
        item["AGENCE_RCS"]=""
        item["SPIRED_ID"]=""
        item["vat_number"]=""
        item["ipi_number"]=""
        #if re.findall('data-type="company"',response.text):
        #    item["SELLER_TYPE"] = "COMPANY"
        #    item["PRO_IND"] = 'Y'
        #else:
        #    item["SELLER_TYPE"] = "Professional"
        #    item["PRO_IND"] = 'N'
        # ==> DONE
        idcompany = ' '.join(re.findall('"propertyCompanyIdDimension":(.*,?)',response.text)).split(",")[0]
        if idcompany == 'null':
            item["SELLER_TYPE"] = "USER"
            item["PRO_IND"] = 'N'
            item["MINI_SITE_URL"]= ""
            item["MINI_SITE_ID"]= ""
            item["AGENCE_NOM"]= ""
            item["AGENCE_CP"]= ""
            item["AGENCE_VILLE"]= ""
            item["AGENCE_ADRESSE"]= ""
            yield item

        else:
            #item["SELLER_TYPE"] = "Professional"
            #item["PRO_IND"] = 'Y'
            mini_site_url = response.xpath("//div[@class='row name']/a/@href").get()
            if mini_site_url:
                url = "https://www.realo.be" + mini_site_url
                item["MINI_SITE_URL"] = url
                item["MINI_SITE_ID"] = idcompany
                item["SELLER_TYPE"] = "Professional"
                item["PRO_IND"] = 'Y'
                yield scrapy.Request(url=url,callback=self.parse_dealer, dont_filter=True,meta={'item':item})
            else:
                js = response.xpath('//script[@type="text/component"]/text()[contains(.,"company-name")]').extract_first()
                if js:
                    js = js.replace('\n','').replace('\t','')
                    name = re.findall('<span class="company-name">(.*?)</span>', js)[0]
                    name = name.lower().replace(' ','-')
                    url = "https://www.realo.be/fr/agence/" + name + "/" + idcompany
                    item["MINI_SITE_URL"] = url
                    item["MINI_SITE_ID"] = idcompany
                    item["SELLER_TYPE"] = "Professional"
                    item["PRO_IND"] = 'Y'
                    yield scrapy.Request(url=url,callback=self.parse_dealer, dont_filter=True,meta={'item':item})        
                else:
                    yield item
            
    def parse_dealer(self, response):
        item = response.meta['item']
        item["AGENCE_NOM"] = response.xpath('//div[@class="col name"]/h2/text()').extract_first().strip()
        try:
            item["WEBSITE"] = response.xpath('//ul[@class="list-unstyled list"]/li/a[@class[contains(.,"icn-globe")]]/text()').extract_first()
        except:
            pass
        ad = response.xpath('//ul/li/p[descendant::i[@class="icn-marker"]]/text()').extract_first()
        if ad:
            ad = ad.split(',')
            if len(ad) == 3:
                item["AGENCE_ADRESSE"] = ad[0].strip()
                item["AGENCE_CP"]= ad[1].strip().split(" ")[0]
                item["AGENCE_VILLE"] = ' '.join(ad[1].strip().split(" ")[1:])
                item["PROVINCE"] = ad[2].strip()
            elif len(ad) == 2:
                item["AGENCE_ADRESSE"] = ad[0].strip()
                item["AGENCE_CP"]= ad[1].strip().split(" ")[0]
                item["AGENCE_VILLE"] = ' '.join(ad[1].strip().split(" ")[1:])
            else:
                item["AGENCE_ADRESSE"] = ''
                item["AGENCE_CP"]= ''
                item["AGENCE_VILLE"] = ''   
        yield item    
