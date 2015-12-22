#!/usr/bin/env python
# -*- coding: utf-8 -*-

from get_descr import parse_item
from lxml import html
import requests
from copy import copy
import csv
import re

# global variables
auth_data = {'login_name': 'fileo@dvhb.ru',
			 'login_password': 'hv8b390h7yw',
			 'login': 'submit'}

site_url = "http://www.fileo-inter.ru"
katalog_url = "/katalog/%s/%s"
# katalog_url = "/katalog/"

catalog = {'yubki': ('plissirovannye-yubki', 'yubki-novinki', 'yubki-klassicheskie', 'yubki-molodezhnye', 'yubki-pryamye', 'yubki-raskleshennye', 'dlinnye-yubki', 'yubki-dlya-polnyh', 'yubki-zauzhennye'),
		   'briuki': ('bryuki-novinki', 'bryuki-klassika', 'bryuki-molodezhnye', 'bryuki-zauzhennye', 'bryuki-pryamye', 'bryuki-legginsy', 'bryuki-7-8'),
		   'platia': ('platya-novinki', 'platya-povsednevnye', 'platya-vechernie', 'platya-dlinnye', 'platya-letnie', 'platya-dlya-polnyh'),
		   'zhilety': (),
		   'sarahfany': (),
		   'bluzy': (),
		   'novyy-god-2016': ()}

# global session object
SESSION = requests.session()

# try to authorize
res = SESSION.post(site_url, data=auth_data).text
HTMLtree = html.document_fromstring(res)

# set cookie for remove pagination
SESSION.post(site_url + katalog_url, data={"show_all": 1})

if HTMLtree.xpath('//*[@class="top_text"]/following-sibling::a/text()')[0] == u'Регистрация':
	print "Authorization failed"
	exit()

# global list
a_res = []

# debug collect result into list
# for x in parse_item(SESSION, 'http://www.fileo-inter.ru/katalog/yubki/yubki-pryamye/', 'yubki', 'yubki-pryamye'):
# 	a_res.append(x)

# try to get catalogue of goods
for x in catalog:
	a_url = site_url + katalog_url % (x, '')
	print a_url
	for y in catalog[x]:
		a_url = site_url + katalog_url % (x, y)
		print a_url

exit()

# try to dublicate sizes
b_res = []
for x in a_res:
	tmp = re.search('(\d{2})-(\d{2})', x['size'])
	if tmp:
		_from, _to = int(tmp.group(1)), int(tmp.group(2)) + 1
		for y in range(_from, _to):
			if (y % 2 == 0):
				x['size'] = str(y)
				b_res.append(copy(x))
	else:
		b_res.append(x)

# export all results into CSV
fields = ['name', 'category', 'subcategory', 'article_in', 'size', 'length', 'price', 'cloth', 'cloth_code', 'cloth_color', 'cloth_img', 'content', 'describe', 'article_out', 'is_new', 'is_sale', 'img_mini', 'img1', 'img2', 'img3']
writer = csv.DictWriter(open('img/import.csv', 'wb'), fieldnames=fields, delimiter=';')
writer.writeheader()

for x in b_res:
	writer.writerow({y:z.encode('utf-8') for y,z in x.items()})