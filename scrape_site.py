# verbose scraper - paste into scraper\scrape_site.py
import requests
from bs4 import BeautifulSoup
import csv
import os
import sys
import time

# --- Edit the URLs to pages you want to scrape ---
URLS = [
    "https://www.kaggle.com/datasets/joshfjelstul/world-cup-database"  # safe test site
]

OUT_DIR = os.path.join("data", "raw")
OUT_FN = os.path.join(OUT_DIR, "scraper_output.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DataCollectionBot/1.0; +mailto:your-email@example.com)"
}

def fetch(url):
    print(f"Fetching: {url}")
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    time.sleep(1)  # polite pause
    return r.text

def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    countries = soup.select("div.country")
    data = []
    for c in countries:
        name_el = c.select_one(".country-name")
        capital_el = c.select_one(".country-capital")
        name = name_el.get_text(strip=True) if name_el else ""
        capital = capital_el.get_text(strip=True) if capital_el else ""
        data.append({"country": name, "capital": capital})
    return data

def main():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
        print(f"Created folder: {OUT_DIR}")

    all_data = []
    for url in URLS:
        try:
            html = fetch(url)
            rows = parse(html)
            print(f"  -> Found {len(rows)} rows on this page.")
            all_data.extend(rows)
        except Exception as e:
            print("ERROR fetching/parsing", url, e, file=sys.stderr)

    if not all_data:
        print("No data collected. Exiting without writing a file.")
        return

    fieldnames = list(all_data[0].keys())
    with open(OUT_FN, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)
    print(f"Wrote {len(all_data)} rows to {OUT_FN}")

if __name__ == "__main__":
    main()
