import requests
import csv
import time

# OLX internal API URL
base_url = "https://www.olx.in/api/relevance/v2/search"

# Parameters for car cover search
params = {
    "query": "car cover",
    "platform": "web-desktop",
    "location": 1000001,  # All India
    "lang": "en",
    "page": 0
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36"
}

# CSV output file
csv_file = open("olx_car_covers.csv", "w", newline='', encoding="utf-8")
writer = csv.DictWriter(csv_file, fieldnames=["Title", "Price", "Location", "Date Posted", "Item URL"])
writer.writeheader()

while True:
    print(f"Scraping page {params['page']}...")
    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch data.")
        break

    data = response.json().get("data", [])
    if not data:
        print("No more data.")
        break

    for item in data:
        title = item.get("title", "N/A")
        price = item.get("price", {}).get("value", {}).get("display", "N/A")
        location = item.get("locations_resolved", {}).get("ADMIN_LEVEL_3_name", "N/A")
        date_posted = item.get("display_date", "N/A")
        item_id = item.get("id", "N/A")
        url = f"https://www.olx.in/item/-iid-{item_id}"

        writer.writerow({
            "Title": title,
            "Price": price,
            "Location": location,
            "Date Posted": date_posted,
            "Item URL": url
        })

    params["page"] += 1
    time.sleep(1)  # Be polite!

csv_file.close()
print("✅ Data saved to olx_car_covers.csv")
