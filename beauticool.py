import requests
from bs4 import BeautifulSoup
import csv
import re
import sys

# ดึงข้อมูลจากเว็บไซต์ beauticool
page = requests.get('https://www.beauticool.com/m/category.php?cat=3&p=1#pn')
sys.stdout.reconfigure(encoding='utf-8') # กำหนดให้รองรับ UTF-8
soup = BeautifulSoup(page.content, 'html.parser')
#print(page)

# ดึงข้อมูลชื่อสินค้า
product_names = soup.find_all(class_='product2-text')
product_list = []
for product in product_names:
    # ลบ strong tag ทั้งหมดใน element นี้
    for strong_tag in product.find_all('strong'):
        strong_tag.decompose()  # ลบ strong tag ออกไป
    product_list.append(product.get_text().strip())
# print(product_list)

# list สำหรับแยกข้อความภาษาไทยและอังกฤษ
english_products = []
thai_products = []

# function ในการแยกข้อความภาษาไทยกับอังฤษ
def split_english_thai(text):
    for index, char in enumerate(text):
        if re.match(r'[ก-๙]', char):
            return text[:index].strip(),text[index:].strip()

# แยกชื่อสินค้าระหว่างภาษาไทยกับอังกฤษ
for product in product_list:
    english_part, thai_part = split_english_thai(product)
    english_products.append(english_part.strip())
    thai_products.append(thai_part.strip())
#print(english_products)
#print(thai_products)



# หา element ที่มีราคาที่ลดและราคาปกติ
products = soup.find_all('div', class_='product2-price-circle')

# จัดเก็บผลลัพธ์แยกเป็น 2 คอลัมน์: prices และ sale
prices_list = []
sales_list = []

for product in products:
    prices = product.find('span', class_='txt-full-price')
    sale = product.find('span', class_='txt-price')

    prices = prices.get_text(strip=True) if prices else '-'
    sale = sale.get_text(strip=True) if sale else '-'

    prices_list.append(prices)
    sales_list.append(sale)

# แสดงผลลัพธ์ที่แยกกัน
#print(prices_list)
#print(sales_list)

# ดึงข้อมูลโปรโมชั่น
# ค้นหา elements ทั้งหมดที่มีคลาส product2-detail และ product2
details = soup.find_all(class_='product2-detail')
names = soup.find_all(class_='product2')
promotion_list = []

# ตรวจสอบ element จาก class product2-detail สำหรับ flash sale
for detail in details:
    img_tag = detail.find('img')
    if img_tag and 'src' in img_tag.attrs:
        promotion_list.append('flash sale')
    else:
        promotion_list.append('-')  # ในกรณีที่ไม่มี img ใน product2-detail

# ตรวจสอบ element จาก class product2 สำหรับ big sale
for name in names:
    if '-' in promotion_list:  # ตรวจสอบว่าในผลลัพธ์มี "-" อยู่แล้วหรือไม่
        sign_tag = name.find(class_='sign signtop--bigsale')
        if sign_tag:
            # แทนที่ "-" ที่ตรวจพบด้วย "big sale"
            promotion_list[promotion_list.index('-')] = 'big sale'
#print(promotion_list)

# ดึงข้อมูลยอดขายสินค้า
sold = soup.find_all(class_='product2-bottom')
sold_list = [sold.get_text().strip().split(' ')[-1] for sold in sold]
#print(sold_list)

# สร้าง text file
with open('product_prices.txt', 'w', encoding='utf-8') as f:
    for english, prices, sale, promotion, sold in zip(english_products, prices_list, sales_list, promotion_list, sold_list):
        f.write(english + '\t' +  prices + '\t' + sale + '\t' + promotion + '\t' + sold + '\n')
print("Data saved to products.txt")

# สร้าง .csv file
with open('product_prices.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Product_names', 'Prices', 'Sales', 'Promotion', 'Sold_out'])
    for english, prices, sale, promotion, sold in zip(english_products, prices_list, sales_list, promotion_list, sold_list):
        writer.writerow([english, prices, sale, promotion, sold])
print("Data saved to products.csv")
