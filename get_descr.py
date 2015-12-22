#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
from get_img import download_img
import requests
import re


def isNew(obj):
	if obj:
		return '+'
	return '-'


def isSale(p_str):
	if p_str == 'sale':
		return '+'
	return '-'


def get_img_from_url(p_url):
	return re.search('([^\/]+)$', p_url).group(0)


def parse_item(p_session, p_url, p_category, p_subcategory):
	site_url = "http://www.fileo-inter.ru"

	catalog_rus = { 'yubki': u'Юбки',
					'plissirovannye-yubki': u'Плиссированные',
					'yubki-novinki': u'Новинки',
					'yubki-klassicheskie': u'Классические',
					'yubki-molodezhnye': u'Молодёжные',
					'yubki-pryamye': u'Прямые',
					'yubki-raskleshennye': u'Расклешённые',
					'dlinnye-yubki': u'Длинные',
					'yubki-dlya-polnyh': u'Для полных',
					'yubki-zauzhennye': u'Зауженные',
					'briuki': u'Брюки',
					'bryuki-novinki': u'Новинки',
					'bryuki-klassika': u'Класика',
					'bryuki-molodezhnye': u'Молодёжные',
					'bryuki-zauzhennye': u'Зауженные',
					'bryuki-pryamye': u'Прямые',
					'bryuki-legginsy': u'Леггинсы',
					'bryuki-7-8': u'7/8',
					'platia': u'Платья',
					'platya-novinki': u'Новинки',
					'platya-povsednevnye': u'Повседневные',
					'platya-vechernie': u'Вечерние',
					'platya-dlinnye': u'Длинные',
					'platya-letnie': u'Летние',
					'platya-dlya-polnyh': u'Для полных',
					'zhilety': u'Жилеты',
					'sarahfany': u'Сарафаны',
					'bluzy': u'Блузы',
					'novyy-god-2016': u'Новый год 2016',
					'': '' }

	items = []
	item = {}

	# try to get url content
	# p_session.get(p_url)
	# HTMLtree = p_session.post(p_url, data = {"show_all": 1}).text
	HTMLtree = p_session.get(p_url).text
	HTMLtree = html.document_fromstring(HTMLtree)

	# get all goods div's
	#goods = HTMLtree.xpath('//*[@class="good_item"]')
	goods = HTMLtree.xpath('//*[contains(@class, "good_item")]')

	print '-' * 100

	# try to get item information
	for good in goods:
		#  get item's personal page html
		item_url = good.xpath('*[@class="good_title"]/@href')[0]
		HTMLtree = p_session.get(site_url + item_url).text
		HTMLtree = html.document_fromstring(HTMLtree)

		# dirty hacks
		item_name = HTMLtree.xpath('//*[@class="good_content"]/h3/text()')[0].strip()
		item_mini_photo = good.xpath('*[@class="good_clotharea"]/following-sibling::img/@src')[0]	
		item_colors = HTMLtree.xpath('//*[contains(./@id, "popup_cloth_info")]/ul/li[2]/text()')
		item_new = isNew(good.xpath('*[@class="good_new"]'))
		item_sale = isSale(p_category)

		item_photos = [re.sub('[^0-9]', '', x)
					   for x in HTMLtree.xpath('//*[contains(@onclick, "setCloth")]/@onclick')]
		item_photos_src = []
		for x in item_photos:
			item_photos_src.append(HTMLtree.xpath(
				'//*[@id="photos%s"]/a/img/@src' % x))

		# check clothes photo and article
		for cloth in enumerate(HTMLtree.xpath('//*[@class="good_cloth"]/div')):
			print u'Название: ' + item_name
			item['name'] = item_name

			print u'Категория: ' + catalog_rus[p_category]
			item['category'] = catalog_rus[p_category]

			print u'Подкатегория: ' + catalog_rus[p_subcategory]
			item['subcategory'] = catalog_rus[p_subcategory]

			tmp = cloth[1].xpath('*[@class="cloth_info"]/p[1]/span/b/text()')

			print u'Артикул вход.: ' + tmp[0]
			item['article_in'] = tmp[0]

			print u'Размеры: ' + tmp[1]
			item['size'] = tmp[1]

			print u'Длина: ' + re.sub('[^0-9]', '', tmp[2])
			item['length'] = re.sub('[^0-9]', '', tmp[2])

			print u'Цена: ' + re.sub('[^0-9]', '', tmp[3])
			item['price'] = re.sub('[^0-9]', '', tmp[3])

			_cloth = cloth[1].xpath('*[@class="cloth_photo"]/p/span[1]/text()')[0]
			print u'Ткань: ' + _cloth
			item['cloth'] = _cloth

			_cloth_code = cloth[1].xpath('*[@class="cloth_photo"]/img/@alt')[0]
			print u'Код ткани: ' + _cloth_code
			item['cloth_code'] = _cloth_code

			print u'Цвет ткани: ' + item_colors[cloth[0]]
			item['cloth_color'] = item_colors[cloth[0]]

			_cloth_img_url = re.sub('_a.jpg$', '_c.jpg', cloth[1].xpath(
				'*[@class="cloth_photo"]/img/@src')[0])
			download_img(_cloth_img_url)
			_cloth_img = get_img_from_url(_cloth_img_url)
			print u'Картинка ткани: ' + _cloth_img
			item['cloth_img'] = _cloth_img

			_content = re.sub(
				'^[^:]+:<br/>', '', ','.join(cloth[1].xpath('*[@class="cloth_info"]/p[2]/span/text()')))
			print u'Состав: ' + _content
			item['content'] = _content

			try:
				_describe = cloth[1].xpath('//*[@id="good_tabs"]/p[1]/text()')[0].strip()
			except:
				_describe = ''
			finally:
				print u'Описание: ' + _describe
				item['describe'] = _describe

			_article_out = '-'.join([tmp[0], cloth[1].xpath(
				'*[@class="cloth_photo"]/img/@alt')[0], tmp[1]])
			print u'Артикул исход.: ' + _article_out
			item['article_out'] = _article_out

			print u'Новинка: ' + item_new
			item['is_new'] = item_new

			print u'Распродажа: ' + item_sale
			item['is_sale'] = item_sale

			_cloth_img_mini_url = item_mini_photo
			_cloth_img_mini = get_img_from_url(_cloth_img_mini_url)
			print u'Фото мини: ' + _cloth_img_mini
			item['img_mini'] = _cloth_img_mini
			download_img(_cloth_img_mini_url)

			tmp = len(item_photos_src[cloth[0]])
			if tmp > 0:
				_img1_url = re.sub('_a.jpg$', '_d.jpg',
								   item_photos_src[cloth[0]][0])
				_img1 = get_img_from_url(_img1_url)
				print u'Фото1: ' + _img1
				item['img1'] = _img1
				download_img(_img1_url)

			if tmp == 2:
				_img2_url = re.sub('_a.jpg$', '_d.jpg',
								   item_photos_src[cloth[0]][1])
				_img2 = get_img_from_url(_img2_url)
				print u'Фото2: ' + _img2
				item['img2'] = _img2
				download_img(_img2_url)

			if tmp == 3:
				_img3_url = re.sub('_a.jpg$', '_d.jpg',
								   item_photos_src[cloth[0]][2])
				_img3 = get_img_from_url(_img3_url)
				print u'Фото3: ' + _img3
				item['img3'] = _img3
				download_img(_img3_url)

			items.append(item)
			item = {}
			print '-' * 100

		# quit after one pass
		return items