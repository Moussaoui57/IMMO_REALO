# REALO
# How to launch a spider
 - Create a virtualEnv Python3.5 
 - Install all libraries that exists in the file `requirements.txt`
 - Launch `Extract_links.py`
 - Drop all duplicated rows based on field ID_CLIENT

Postprocessing :
1- realo_cleaning : Generate Three link files.txt (projet,immeuble,avendre/alouer )
2- /home/h.moussaoui/Realo/Realo/spiders/spider_projet.py : Extract all Project ads.
3- /home/h.moussaoui/Realo/Realo/spiders/spider_listing.py : Extract all to Buy/to Rent ads.
4- /home/h.moussaoui/Realo/Realo/spiders/spider_immeuble.py : Extract all Immeuble Ads.


## Follow this steps

- Install libraries in VirtualEnv
```
pip install -r requirements.txt
```
- Launch a spider `Extract_links.py` in Screen
``` 
scrapy crawl name_of_spider -o name_file_links.txt

- Launch all spiders  in Screen
``` 
scrapy crawl name_of_spider -o name_file_csv.csv
```
- Drop duplicate
```
sort -u -k3,3 -t";" name_file_csv.csv > file_without_dup.csv
```
# IMMO_REALO
