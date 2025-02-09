import os
import sqlite3
import pandas as pd
import bar_chart_race as bcr
import matplotlib
import matplotlib.font_manager as fm

# -----------------------
# 1) กำหนดฟอนต์ไทยสำหรับ Matplotlib
# -----------------------
font_path = r"C:\Windows\Fonts\angsana.ttc"
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    matplotlib.rcParams['font.family'] = font_prop.get_name()
else:
    matplotlib.rcParams['font.family'] = 'Arial Unicode MS'

matplotlib.rcParams['figure.facecolor'] = 'white'
matplotlib.rcParams['savefig.facecolor'] = 'white'
matplotlib.rcParams['axes.unicode_minus'] = False

# -----------------------
# 2) อ่านข้อมูลจากฐานข้อมูล SQLite
# -----------------------
DB_PATH = "../data/trade_data.db"

conn = sqlite3.connect(DB_PATH)
query = """
    SELECT year_month, items_name, items_baht_amnt_import
    FROM trade
    WHERE year >= 2015
"""
df = pd.read_sql_query(query, conn)
conn.close()

# -----------------------
# 3) เตรียม DataFrame ให้เหมาะสมกับ bar_chart_race
# -----------------------
df["year_month"] = pd.to_datetime(df["year_month"], errors="coerce")
df = df.pivot(index="year_month", columns="items_name", values="items_baht_amnt_import")
df = df.fillna(0)
df = df.sort_index()

# -----------------------
# 4) สร้าง Bar Chart Race และบันทึกเป็น GIF
# -----------------------
bcr.bar_chart_race(
    df=df,
    filename="bcr_import.gif",  # ✅ เปลี่ยนชื่อไฟล์ให้เป็น Import
    orientation="h",
    sort="desc",
    n_bars=10,
    period_length=800,
    steps_per_period=10,
    figsize=(6, 4),
    writer='pillow',
    title='Bar Chart Race - ยอดนำเข้า',
)

print("✅ สร้าง bcr_import.gif เรียบร้อย!")
