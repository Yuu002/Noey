import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# โหลดข้อมูลจากไฟล์ CSV
data = pd.read_csv('products_prices.csv')

# ทำความสะอาดข้อมูล: แปลงราคาจากสตริงเป็นตัวเลข, เอาสัญลักษณ์ '฿' ออก และแปลงเป็น float
data['prices'] = data['prices'].replace('-', np.nan).str.replace('฿', '').str.replace(',', '').astype(float)
data['sale'] = data['sale'].replace('-', np.nan).str.replace('฿', '').str.replace(',', '').astype(float)
data['sales_volume'] = data['sales_volume'].replace('-', np.nan).astype(float)

# ลบข้อมูลที่มีค่า NaN หรือข้อมูลที่ไม่ครบถ้วน
data_clean = data.dropna()

# สร้างฟีเจอร์ใหม่: ราคาที่ลด
data_clean['discount'] = data_clean['prices'] - data_clean['sale']

# สร้างโมเดล Linear Regression เพื่อพยากรณ์ยอดขายตามราคาที่ลด
X = data_clean[['sale']]  # ราคาที่ลดเป็นตัวแปรอิสระ (Independent Variable)
y = data_clean['sales_volume']  # ยอดขายเป็นตัวแปรตาม (Dependent Variable)

# สร้างโมเดลการถดถอยเชิงเส้น (Linear Regression)
model = LinearRegression()
model.fit(X, y)

# ดูความสัมพันธ์ระหว่างราคาที่ลดและยอดขาย
plt.figure(figsize=(10, 6))
sns.scatterplot(x='sale', y='sales_volume', data=data_clean, color='blue', label='Actual Sales')
plt.plot(data_clean['sale'], model.predict(X), color='red', label='Predicted Sales')
plt.xlabel('Discounted Price')
plt.ylabel('Sales Volume')
plt.title('Relationship between Discounted Price and Sales Volume')
plt.legend()
plt.show()

# ทำนายยอดขายที่ราคาต่างๆ (Optimal Pricing)
prices_range = np.linspace(data_clean['sale'].min(), data_clean['sale'].max(), 100)
predicted_sales = model.predict(prices_range.reshape(-1, 1))

# หา optimal price ที่ทำให้ยอดขายมากที่สุด
optimal_price_index = np.argmax(predicted_sales)
optimal_price = prices_range[optimal_price_index]

print(f"ราคาที่เหมาะสมที่สุดเพื่อเพิ่มยอดขายคือ: {optimal_price:.2f}฿")