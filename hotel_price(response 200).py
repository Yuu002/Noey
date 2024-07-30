import requests
from bs4 import BeautifulSoup

page = requests.get('https://th.trip.com/hotels/list?city=359')
#print(page)

soup = BeautifulSoup(page.content, 'html.parser')
content = soup.find_all(class_='name')
content = str(content)

hotel_names = soup.find_all(class_='name')
hotel_list = [hotel.get_text() for hotel in hotel_names]
#print(hotel_list)

rating = soup.find_all(class_='inherit')
rating_list = [rating.get_text() for rating in rating]
#print(rating_list)

prices = soup.find_all(class_='real labelColor')
prices_list = [prices.get_text() for prices in prices]
#print(prices_list)

with open('hotel_prices2.txt', 'w', encoding='utf-8') as f:
    for hotel, rating, prices in zip(hotel_list, rating_list, prices_list):
        f.write(hotel + '\t' + rating + '\t' + prices + '\n')
