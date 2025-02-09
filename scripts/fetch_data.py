import sqlite3
import requests
import json
import os

BASE_URL = "https://data.go.th/api/3/action/datastore_search"
RESOURCE_ID = "96075612-8ef4-452a-9e68-eae7ea74166b"
MAX_PAGES = 20  # i = 0 to 20

# ตรวจสอบและสร้างโฟลเดอร์ ../data หากไม่มี
DATA_DIR = "../data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# สร้างการเชื่อมต่อกับ SQLite
conn = sqlite3.connect(os.path.join(DATA_DIR, "trade_data.db"))
cursor = conn.cursor()

# สร้างตารางหากยังไม่มี
cursor.execute('''
    CREATE TABLE IF NOT EXISTS trade (
        id INTEGER PRIMARY KEY,
        year_month TEXT,
        year INTEGER,
        month INTEGER,
        month_name TEXT,
        items_cat_id INTEGER,
        items_name TEXT,
        items_baht_amnt_import INTEGER,
        items_baht_amnt_export INTEGER,
        items_baht_amnt_balance INTEGER,
        color TEXT
    )
''')

# วนลูปดึงข้อมูลทีละ 100 รายการ
for i in range(21):  # Loop from 0 to 20
    offset = 100 * i
    params = {
        "resource_id": RESOURCE_ID,
        "offset": offset
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        records = data.get("result", {}).get("records", [])
        
        if not records:
            print(f"No records found at offset={offset}, stopping.")
            break
        
        # แทรกข้อมูลลงในตาราง SQLite
        for record in records:
            cursor.execute('''
                INSERT INTO trade (
                    id, year_month, year, month, month_name, items_cat_id, 
                    items_name, items_baht_amnt_import, items_baht_amnt_export, 
                    items_baht_amnt_balance, color
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record["_id"], record["year_month"], record["year"], record["month"], 
                record["month_name"], record["items_cat_id"], record["items_name"], 
                record["items_baht_amnt_import"], record["items_baht_amnt_export"], 
                record["items_baht_amnt_balance"], record["color"]
            ))
        
        print(f"Fetched and inserted {len(records)} records from offset={offset}")
    else:
        print(f"Failed to fetch data at offset={offset}: {response.status_code}")
        break

# บันทึกข้อมูลและปิดการเชื่อมต่อ
conn.commit()
conn.close()

print("All data successfully inserted into SQLite database in '../data' folder.")