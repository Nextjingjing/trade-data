import os
import sqlite3

import pandas as pd
import bar_chart_race as bcr

import matplotlib
import matplotlib.font_manager as fm

# -----------------------
# 1) กำหนดฟอนต์ไทยสำหรับ Matplotlib
# -----------------------
# ตัวอย่างใช้ Angsana New (angsana.ttc) ซึ่งเป็นฟอนต์ไทยใน Windows
font_path = r"C:\Windows\Fonts\angsana.ttc"  
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    matplotlib.rcParams['font.family'] = font_prop.get_name()
else:
    # สำรอง: ถ้าไม่มีฟอนต์ Angsana ให้ใช้ Arial Unicode MS หรือฟอนต์สากลที่รองรับไทย
    matplotlib.rcParams['font.family'] = 'Arial Unicode MS'

# ตั้งค่าว่าให้ใช้พื้นหลังสีขาว (กันปัญหาพื้นหลังใส)
matplotlib.rcParams['figure.facecolor'] = 'white'
matplotlib.rcParams['savefig.facecolor'] = 'white'

# ให้เครื่องหมายลบ (-) แสดงได้ถูกต้อง
matplotlib.rcParams['axes.unicode_minus'] = False

# -----------------------
# 2) อ่านข้อมูลจากฐานข้อมูล SQLite
# -----------------------
DB_PATH = "../data/trade_data.db"  # ปรับตามตำแหน่งไฟล์จริง

conn = sqlite3.connect(DB_PATH)
query = """
    SELECT year_month, items_name, items_baht_amnt_export
    FROM trade
    WHERE year >= 2015
"""
df = pd.read_sql_query(query, conn)
conn.close()

# -----------------------
# 3) เตรียม DataFrame ให้เหมาะสมกับ bar_chart_race
# -----------------------
# - แปลง year_month เป็น datetime
# - pivot ให้ index เป็นวันที่ (DatetimeIndex)
# - คอลัมน์เป็น items_name
# - ค่าเป็น items_baht_amnt_export
df["year_month"] = pd.to_datetime(df["year_month"], errors="coerce")
df = df.pivot(index="year_month", columns="items_name", values="items_baht_amnt_export")

# แทน NaN ด้วย 0
df = df.fillna(0)

# เรียงตามเวลาจากน้อยไปมาก
df = df.sort_index()

# -----------------------
# 4) สร้าง Bar Chart Race และบันทึกเป็น GIF
# -----------------------
bcr.bar_chart_race(
    df=df,                        # DataFrame ที่จัดรูปแบบแล้ว
    filename="barchart_race.gif", # ชื่อไฟล์ GIF
    orientation="h",             # แสดงเป็นแท่งแนวนอน
    sort="desc",                  # เรียงจากค่ามากไปน้อย
    n_bars=10,                    # แสดง 10 อันดับ
    period_length=800,            # ความยาวเวลา(มิลลิวินาที) ในการแสดงแต่ละช่วง
    steps_per_period=10,          # จำนวนเฟรมย่อยต่อช่วง (ยิ่งมากยิ่งลื่น)
    figsize=(6, 4),               # ขนาดภาพ (นิ้ว)
    writer='pillow',              # ใช้ pillow สร้าง GIF (ไม่ต้องใช้ ffmpeg)
    title='Bar Chart Race - ยอดส่งออก',  # ชื่อกราฟ (รองรับไทยเพราะเราตั้งฟอนต์ไว้แล้ว)
)

print("✅ สร้าง barchart_race.gif เรียบร้อย!")
