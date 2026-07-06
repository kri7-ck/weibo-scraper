import requests
import csv
import datetime
import os
import time

def get_weibo_hot_search():
    url = 'https://weibo.com/ajax/side/hotSearch'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://weibo.com/',
        'Origin': 'https://weibo.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    try:
        print("正在请求微博热搜接口...")
        response = requests.get(url, headers=headers, timeout=15)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok') == 1:
                print("✅ 成功获取热搜数据")
                return data.get('data', {})
            else:
                print(f"接口返回异常: {data.get('msg', '未知错误')}")
                return None
        else:
            print(f"HTTP请求失败，状态码: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print("请求超时，请稍后重试")
        return None
    except requests.exceptions.ConnectionError:
        print("网络连接失败，请检查网络")
        return None
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
    print("=" * 40)
    print(f"开始抓取微博热搜 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 40)
    
    data = get_weibo_hot_search()
    if data:
        save_to_csv(data)
    else:
        print("❌ 获取失败，请检查网络或稍后重试")
        # 创建一个空文件标记失败，但仍然保留以便排查
        with open('weibo_hot_history.csv', 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            if not os.path.isfile('weibo_hot_history.csv'):
                writer.writerow(['抓取时间', '状态'])
            writer.writerow([datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '抓取失败'])
