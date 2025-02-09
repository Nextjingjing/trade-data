# Project: Trade Data Analysis & Visualization การนำเข้า-ส่งออกสินค้าฟุ้มเฟือย

## 📌 Overview
This project fetches trade data from an API, stores it in an SQLite database, and visualizes it using bar race charts and other statistical analysis.

## 📌 รันสคริปต์
pip install -r requirements.txt

cd .\scripts\

python fetch_data.py # สร้าง sqlite3 ของข้อมูล

python barchart_race.py # สร้าง gif ของการส่งออก

python brc_import.py # สร้าง gif ของการนำเข้า
