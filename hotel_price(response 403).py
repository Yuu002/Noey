import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/0.5 (Windows NT 5.1) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
url = 'https://www.trivago.co.th/th/odr/%E0%B9%82%E0%B8%A3%E0%B8%87%E0%B9%81%E0%B8%A3%E0%B8%A1-%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8%E0%B9%84%E0%B8%97%E0%B8%A2?search=200-196'
page = requests.get(url, headers=headers)
#print(page)

soup = BeautifulSoup(page.content, 'html.parser')
hotel_names = soup.find_all('h2', class_='Heading_heading__xct3h Heading_h-m__bqwg0 CardContent_accommodationName__a1N1I')
hotel_list = [hotel.get_text() for hotel in hotel_names]
#print(hotel_list)

province_names = soup.find_all('span', class_='CardContent_trimSpace__YzOr1 truncate_truncate__vCzPM')
province_list = [province.get_text() for province in province_names]
#print(province_list)

re_prices = soup.find_all('strong', class_='CardForecastedPrice_priceLabel__ANbuo')
prices_list = [prices.get_text().replace('\xa0', ' ') for prices in re_prices]
#print(prices_list)

with open('hotel_prices1.txt', 'w', encoding='utf-8') as file:
    for hotel, province, prices in zip(hotel_list, province_list, prices_list):
        file.write(hotel + '\t' + province + '\t' + prices + '\n')
