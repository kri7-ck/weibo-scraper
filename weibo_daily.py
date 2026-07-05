import requests
import csv
import datetime
import os

def get_weibo_hot_search():
    url = 'https://weibo.com/ajax/side/hotSearch'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200 and response.json().get('ok') == 1:
            return response.json().get('data', {})
    except Exception as e:
        print(f"抓取失败: {e}")
    return None

def save_to_csv(data):
    file_exists = os.path.isfile('weibo_hot_history.csv')
    with open('weibo_hot_history.csv', 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['抓取时间', '排名', '关键词', '热度', '标签'])
        
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        realtime = data.get('realtime', [])
        for idx, item in enumerate(realtime, 1):
            writer.writerow([
                now,
                idx,
                item.get('word', ''),
                item.get('raw_hot', item.get('num', '')),
                item.get('icon_desc', '')
            ])
    print(f"✅ 数据已保存，共 {len(realtime)} 条")

if __name__ == "__main__":
    data = get_weibo_hot_search()
    if data:
        save_to_csv(data)
    else:
        print("❌ 获取失败")