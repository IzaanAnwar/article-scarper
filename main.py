import sqlite3
import time
import pandas as pd
import requests
import pprint as pp
import bs4
import flask
import json
from flask import jsonify

sheet_df = pd.read_excel("sheet.xlsx")
conn = sqlite3.connect("article.db")
cursor = conn.cursor()


link_lists = sheet_df["Links"].to_list()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS tech (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
    )
"""
)

for index, link in enumerate(sheet_df["Links"]):
    url = f"http://localhost:3000/api/article?url={link}"
    response = requests.get(url=url)
    if response.status_code == 200:
        data = response.json()
        title = data["title"]
        content = data["content"]
        # pp.pprint(title)
        # pp.pprint(content)
        cursor.execute(
            "INSERT INTO tech (title, content) VALUES (?, ?)", (title, content)
        )

    else:
        print(f"Failed to fetch content for link at index {index}")

conn.commit()
