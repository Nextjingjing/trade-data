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
        year_month TEXT NOT NULL,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        month_name TEXT NOT NULL,
        items_cat_id INTEGER NOT NULL,
        items_name TEXT NOT NULL,
        items_baht_amnt_import INTEGER NOT NULL DEFAULT 0,
        items_baht_amnt_export INTEGER NOT NULL DEFAULT 0,
        items_baht_amnt_balance INTEGER NOT NULL DEFAULT 0,
        color TEXT DEFAULT 'Unknown'
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
        
        # แทรกข้อมูลลงในตาราง SQLite พร้อมทำความสะอาดข้อมูล
        for record in records:
            try:
                record_id = int(record.get("_id", 0))
                if record_id == 0:
                    continue  # ข้ามข้อมูลที่ไม่มี _id

                year_month = str(record.get("year_month", "Unknown"))
                year = int(record.get("year", 0))
                month = int(record.get("month", 0))
                month_name = str(record.get("month_name", "Unknown")).strip()
                items_cat_id = int(record.get("items_cat_id", 0))
                items_name = str(record.get("items_name", "Unknown")).strip()
                
                # ตรวจสอบค่าตัวเลข
                items_baht_amnt_import = max(0, int(record.get("items_baht_amnt_import", 0)))
                items_baht_amnt_export = max(0, int(record.get("items_baht_amnt_export", 0)))
                items_baht_amnt_balance = int(record.get("items_baht_amnt_balance", 0)) 

                # ตรวจสอบค่าสี
                color = record.get("color", "").strip()
                if not color:
                    color = "Unknown"

                # ใช้ INSERT IGNORE หรือ REPLACE เพื่อป้องกันข้อมูลซ้ำ
                cursor.execute('''
                    INSERT OR IGNORE INTO trade (
                        id, year_month, year, month, month_name, items_cat_id, 
                        items_name, items_baht_amnt_import, items_baht_amnt_export, 
                        items_baht_amnt_balance, color
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    record_id, year_month, year, month, month_name, items_cat_id, 
                    items_name, items_baht_amnt_import, items_baht_amnt_export, 
                    items_baht_amnt_balance, color
                ))

            except (ValueError, KeyError, TypeError) as e:
                print(f"Skipping record with error: {e}")

        print(f"Fetched and inserted {len(records)} records from offset={offset}")
    else:
        print(f"Failed to fetch data at offset={offset}: {response.status_code}")
        break

# บันทึกข้อมูลและปิดการเชื่อมต่อ
conn.commit()
conn.close()

print("All data successfully inserted into SQLite database in '../data' folder.")

