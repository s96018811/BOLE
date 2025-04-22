import requests
from bs4 import BeautifulSoup
import json

# 網站網址
url = 'https://news.bolebonus.com/p/404-1111-11784.php'

# 模擬正常瀏覽器的 User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 發送 HTTP 請求
response = requests.get(url, headers=headers)

# 檢查 HTTP 請求是否成功
if response.status_code == 200:
    # 解析頁面
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到每一個新聞項目
    news_items = []
    articles = soup.find_all('div', class_='d-item v-it col-sm-12')

    # 如果找不到任何資料，打印 HTML 結構以進行調試
    if not articles:
        print("No articles found. Check the page structure.")
        print(soup.prettify())  # 打印出頁面結構，便於排查

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
    
    # 保存為 JSON 檔案
    if news_items:
        with open('news_data.json', 'w', encoding='utf-8') as f:
            json.dump(news_items, f, ensure_ascii=False, indent=2)

        print("抓取成功！")
    else:
        print("沒有抓取到任何資料。")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
