import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Use undetected Chrome driver
driver = uc.Chrome()

data = []

for page in range(1, 4):
    print(f"Scraping page {page}...")
    driver.get(f"https://www.olx.in/items/q-car-cover?page={page}")
    time.sleep(5)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@data-aut-id='itemBox']"))
        )
    except:
        print(f"No listings found on page {page}")
        continue

    listings = driver.find_elements(By.XPATH, "//a[@data-aut-id='itemBox']")

    for item in listings:
        full_text = item.text.strip().splitlines()

        title = full_text[0] if len(full_text) > 0 else "N/A"
        price = full_text[1] if len(full_text) > 1 else "N/A"
        location = full_text[2] if len(full_text) > 2 else "N/A"
        date_posted = full_text[3] if len(full_text) > 3 else "N/A"
        url = item.get_attribute("href")

        print("✔️", title, "|", price)

        data.append({
            "Title": title,
            "Price": price,
            "Location": location,
            "Date Posted": date_posted,
            "Item URL": url
        })

driver.quit()

df = pd.DataFrame(data)
df.to_csv("olx_car_covers.csv", index=False, encoding='utf-8')
print("✅ Scraping complete. Data saved to olx_car_covers.csv")
