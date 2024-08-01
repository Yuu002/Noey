import requests
from bs4 import BeautifulSoup
import csv
import re
import sys

# ดึงข้อมูลจากเว็บไซต์ beauticool
page = requests.get('https://www.beauticool.com/m/category.php?cat=1')
sys.stdout.reconfigure(encoding='utf-8') # กำหนดให้รองรับ UTF-8
soup = BeautifulSoup(page.content, 'html.parser')
#print(page)

# ดึงข้อมูลชื่อสินค้า
product_names = soup.find_all(class_='product2-text')
product_list = [product.get_text().strip() for product in product_names]

# list สำหรับแยกข้อความภาษาไทยและอังกฤษ
english_products = []
thai_products = []

# function ในการแยกข้อความภาษาไทยกับอังฤษ
def split_english_thai(text):
    for index, char in enumerate(text):
        if re.match(r'[ก-๙]', char):
            return text[:index].strip(),text[index:].strip()
            return text, ''

# แยกชื่อสินค้าระหว่างภาษาไทยกับอังกฤษ
for product in product_list:
    english_part, thai_part = split_english_thai(product)
    english_products.append(english_part.strip())
    thai_products.append(thai_part.strip())
#print(english_products)
#print(thai_products)

# ดึงข้อมูลราคาสินค้า
prices = soup.find_all(class_='txt-price')
prices_list = [prices.get_text() for prices in prices]
#print(prices_list)

# ดึงข้อมูลยอดขายสินค้า
sold = soup.find_all(class_='product2-bottom')
sold_list = [sold.get_text().strip().split(' ')[-1] for sold in sold]
#print(sold_list)

# สร้าง text file
with open('product_prices.txt', 'w', encoding='utf-8') as f:
    for english, thai, prices, sold in zip(english_products, thai_products, prices_list, sold_list):
        f.write(english + '\t' + thai + '\t' + prices + '\t' + sold + '\n')
print("Data saved to products.txt")

# สร้าง .csv file
with open('product_prices.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Product_eng_names', 'Product_thai_names', 'Prices', 'Sold_out'])
    for english, thai, prices, sold in zip(english_products, thai_products, prices_list, sold_list):
        writer.writerow([english, thai, prices, sold])
print("Data saved to products.csv")
