import os
import re
import time
import sqlite3
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Get SEMrush login details from BitWarden
SEMRUSH_EMAIL = os.getenv("SEMRUSH_USERNAME")
SEMRUSH_PASSWORD = os.getenv("SEMRUSH_PASSWORD")

if not SEMRUSH_EMAIL or not SEMRUSH_PASSWORD:
    print("Error: SEMrush credentials not found in environment variables!")
    exit(1)
 

# Validate websites from command-line arguments
websites = sys.argv[1:]
if not websites:
    print("Usage: python semrush_report.py domain1.com domain2.com ...")
    sys.exit(1)

# Validate domain format
def validate_domain(domain):
    return re.match(r".*?\.[a-z]{2,}$", domain) is not None

websites = [w.lower() for w in websites if validate_domain(w)]
if not websites:
    print("Error: No valid domains provided!")
    sys.exit(1)

# Default SEMrush database
DB_LOCATION = "us"

# Construct SEMrush search URLs
semrush_urls = [f"https://semrush.com/analytics/organic/positions/?db={DB_LOCATION}&searchType=domain&q={w}" for w in websites]

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--lang=en")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def login_to_semrush():
    """Log into SEMrush using Selenium"""
    print("Logging into SEMrush...")
    driver.get("https://www.semrush.com/login")
    
    # Enter email
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(SEMRUSH_EMAIL)
    # Enter password
    driver.find_element(By.NAME, "password").send_keys(SEMRUSH_PASSWORD)
    # Click login button
    driver.find_element(By.CLASS_NAME, "sc-btn__inner").click()
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dashboard-selector")))
        print("Login successful!")
    except:
        print("Login failed. Check credentials.")
        driver.quit()
        sys.exit(1)

def scrape_website_data(url, website):
    """Extract keyword rankings for a website from SEMrush"""
    print(f"Scraping data for: {website}")
    driver.get(url)
    
    try:
        # Check if there's no data
        no_results = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "cl-nothing-found-page__title")))
        print(f"{website}: No ranking data found.")
        return None
    except:
        pass

    # Extract rankings (modify this based on actual table structure)
    try:
        keywords = driver.find_elements(By.CSS_SELECTOR, "tr td:nth-child(1)")  # Adjust selector
        rankings = driver.find_elements(By.CSS_SELECTOR, "tr td:nth-child(2)")  # Adjust selector

        data = []
        for k, r in zip(keywords, rankings):
            keyword = k.text.strip()
            rank = int(r.text.strip()) if r.text.strip().isdigit() else None
            if keyword and rank:
                data.append((website, keyword, rank))

        print(f"{website}: {len(data)} keywords found.")
        return data
    except Exception as e:
        print(f"Error extracting data for {website}: {e}")
        return None

def save_to_database(data):
    """Save scraped data to SQLite"""
    if not data:
        return

    conn = sqlite3.connect("semrush_data.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            keyword TEXT NOT NULL,
            ranking INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.executemany("INSERT INTO reports (website, keyword, ranking) VALUES (?, ?, ?)", data)
    conn.commit()
    conn.close()
    print(f"Saved {len(data)} records to database.")

# Run automation
login_to_semrush()

for website, url in zip(websites, semrush_urls):
    results = scrape_website_data(url, website)
    save_to_database(results)

# Close WebDriver
driver.quit()
print("Scraping complete!")
