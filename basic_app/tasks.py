from celery import shared_task
import requests
import json
print("Loading tasks...")
@shared_task
def fetch_and_save_data():
    print("Fetching and saving data...")
    url = 'https://mentalaba.uz/_next/data/xeDLhkddhAt3SD5lRYiYp/uz/universities/otm-haqida/xalqaro-tmc-instituti.json?about=xalqaro-tmc-instituti'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"{data} fetched and saved successfully.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

fetch_and_save_data()