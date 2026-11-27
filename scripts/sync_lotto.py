#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taiwan Lottery 649 (大樂透) Incremental Sync Script
This script fetches latest draws from the official API and merges them with data/lotto649.json
Safe for execution inside GitHub Actions on a schedule.
"""

import os
import json
import requests
from datetime import datetime, timedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/lotto649.json')
PUBLIC_DATA_FILE = os.path.join(os.path.dirname(__file__), '../public/data/lotto649.json')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Origin': 'https://www.taiwanlottery.com',
    'Referer': 'https://www.taiwanlottery.com/'
}

def load_existing_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    os.makedirs(os.path.dirname(PUBLIC_DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(PUBLIC_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_month(year, month):
    month_str = f"{year}-{month:02d}"
    url = f"https://api.taiwanlottery.com/TLCAPIWeB/Lottery/Lotto649Result?period&month={month_str}&pageSize=50"
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code == 200:
            res = r.json().get('content', {}).get('lotto649Res', [])
            return res
    except Exception as e:
        print(f"Fetch failed for {month_str}: {e}")
    return []

def main():
    existing = load_existing_data()
    existing_map = {item['period']: item for item in existing}
    print(f"Current database has {len(existing)} draws.")

    # Determine months to check: check previous month and current month
    now = datetime.now()
    months_to_check = []
    
    # Check last 3 months to prevent any missing gap
    for offset in range(3, -1, -1):
        target_date = now - timedelta(days=offset * 28)
        ym = (target_date.year, target_date.month)
        if ym not in months_to_check:
            months_to_check.append(ym)

    new_count = 0
    for y, m in months_to_check:
        print(f"Fetching {y}-{m:02d}...")
        draws = fetch_month(y, m)
        for d in draws:
            period = d['period']
            if period not in existing_map:
                existing_map[period] = {
                    'period': period,
                    'date': d['lotteryDate'][:10],
                    'numbers_sorted': d['drawNumberSize'][:6],
                    'special': d['drawNumberSize'][6] if len(d['drawNumberSize']) > 6 else None
                }
                new_count += 1

    merged = list(existing_map.values())
    merged.sort(key=lambda x: (x['date'], x['period']))
    save_data(merged)

    print(f"Sync complete. Added {new_count} new draws. Total in database: {len(merged)}")
    if new_count > 0:
        print(f"Latest draw: Period {merged[-1]['period']} ({merged[-1]['date']}): {merged[-1]['numbers_sorted']} + {merged[-1]['special']}")

if __name__ == '__main__':
    main()
