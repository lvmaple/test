from bs4 import BeautifulSoup
import re
import requests

# url = "https://s.taobao.com/search?q=%E8%A1%AC%E8%A1%A3&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20160916"

headers = {'Host': 's.taobao.com',
           'Connection': 'keep-alive',
           'X - Requested - With': 'ShockwaveFlash / 22.0.0.192',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
           'Content-Type': 'text/html;charset=UTF-8',
           'Accept': "*/*",
           # 'Referer': 'http://static.hdslb.com/live-static/swf/LivePlayerEx_1.swf?2016072301',
           'Accept-Encoding': 'gzip',
           'Accept-Language': 'zh-CN',
           'server': 'Tengine/Aserver'
           }
s = requests.session()

# price = 50

for p in range(1,11):
	price = p * 50

	view_sales = []
	view_fee = []
	view_price = []
	for i in range(100):
		url = "https://s.taobao.com/search?q=%E5%A5%B3%E8%A3%85&imgfile=&js=1&style=grid&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20160916&ie=utf8&bcoffset=-1&ntoffset=-1&p4ppushleft=1%2C48&filter=reserve_price%5B{price}%2C{price_m}%5D&sort=default&s={page}".format(price=str(price), price_m=str(price + 49), page=str(i*44))

		res = s.get(url=url, headers=headers)
		print(url)
		print(res.status_code)
		text = res.text

		text_temp = re.findall(r'\"view_price\".*?\d{1,}人付款\"', text)
		print(text_temp)
		for temp in text_temp:
			sales_temp = re.findall(r'\d{1,}人付款', temp).pop()
			sales_temp = re.findall(r'\d{1,}', sales_temp)

			price_temp = re.findall(r'\"view_price\".*?,', temp).pop()
			price_temp = re.findall(r'\d{1,}\.\d{1,}', price_temp)

			fee_temp = re.findall(r'\"view_fee\".*?,', temp).pop()
			fee_temp = re.findall(r'\d{1,}\.\d{1,}', fee_temp)

			# view_sales.append(sales_temp)
			# view_price.append(price_temp)
			# view_fee.append(fee_temp)

			view_sales += sales_temp
			view_fee += fee_temp
			view_price += price_temp

		# sales_temp = re.findall(r'\d{1,}人付款', "".join(text_temp))
		# # del sales_temp[44:]
		# sales_temp = re.findall(r'\d{1,}', "".join(sales_temp))

		# price_temp = re.findall(r'\"view_price\".*?,', "".join(text_temp))
		# # del price_temp[44:]
		# price_temp = re.findall(r'\d{1,}\.\d{1,}', "".join(price_temp))

		# fee_temp = re.findall(r'\"view_fee\".*?,', "".join(text_temp))
		# # del fee_temp[44:]
		# fee_temp = re.findall(r'\d{1,}\.\d{1,}', "".join(fee_temp))

		# view_sales += sales_temp
		# view_fee += fee_temp
		# view_price += price_temp

		print(view_fee)
		print(len(view_sales))
		print(len(view_price))

	free_sales = []
	free_price = []
	free_n_sales = []
	free_n_price = []

	for index,item in enumerate(view_fee):
		if float(item) == 0:
			# if len(free_sales) <= 300:
			free_sales.append(view_sales[index])
			free_price.append(view_price[index])
		else:
			# if len(free_n_sales) <= 300:
			free_n_sales.append(view_sales[index])
			free_n_price.append(view_price[index])

	fp = open("tb\\free_{price}".format(price=price),'w+')
	fp1 = open("tb\\free_n_{price}".format(price=price),'w+')

	for index,item in enumerate(free_price):
		fp.write(item + ":" + free_sales[index] + "\n")

	for index,item in enumerate(free_n_price):
		fp1.write(item + ":" + free_n_sales[index] + "\n")

	fp.close()
	fp1.close()

