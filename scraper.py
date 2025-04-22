import os
import requests
from bs4 import BeautifulSoup
import json

# 檢查資料夾是否存在，若不存在則創建
if not os.path.exists('data'):
    os.makedirs('data')

# 網站網址
url = 'https://news.bolebonus.com/p/404-1111-11784.php'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 找到每一個新聞項目
news_items = []
articles = soup.find_all('div', class_='d-item v-it col-sm-12')

for article in articles:
    title_tag = article.find('a', title=True)  # 找到有標題的 <a> 標籤
    image_tag = article.find('img')  # 找到圖片 <img> 標籤
    
    if title_tag and image_tag:
        title = title_tag['title'].strip()  # 取得標題
        link = title_tag['href']  # 取得連結
        image = image_tag['src']  # 取得圖片

        # 處理圖片的相對路徑，轉換成絕對路徑
        if image.startswith('/'):
            image = 'https://news.bolebonus.com' + image
        
        news_items.append({
            'title': title,
            'url': link,
            'image': image
        })

# 儲存為 JSON 檔案
with open('data/news_data.json', 'w', encoding='utf-8') as f:
    json.dump(news_items, f, ensure_ascii=False, indent=2)

print("抓取成功！")
