import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Initialize SQLite DB
conn = sqlite3.connect("semrush_data.db")
cursor = conn.cursor()

# Setup Chrome WebDriver
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Visit SEMrush
driver.get("https://www.semrush.com")
title = driver.title

# Store data in SQLite
cursor.execute("INSERT INTO reports (keyword, ranking) VALUES (?, ?)", ("example", 1))
conn.commit()

# Cleanup
driver.quit()
conn.close()

print("Data saved to SQLite!")
