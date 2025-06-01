import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

# Launch Chrome
driver = uc.Chrome()

# Store results here
results = []

# Set number of pages you want to scrape
max_pages = 10  # Change to 20, 50, etc., if you want more

try:
    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")
        url = f"https://www.yellowpages.com/search?search_terms=electrician&geo_location_terms=Los+Angeles%2C+CA&page={page}"
        driver.get(url)
        time.sleep(3)  # Let the page load fully

        listings = driver.find_elements(By.CLASS_NAME, "result")

        for listing in listings:
            try:
                name = listing.find_element(
                    By.CLASS_NAME, "business-name").text
            except:
                name = ""

            try:
                phone = listing.find_element(
                    By.CLASS_NAME, "phones.phone.primary").text
            except:
                phone = ""

            try:
                address1 = listing.find_element(
                    By.CLASS_NAME, "street-address").text
            except:
                address1 = ""

            try:
                address2 = listing.find_element(By.CLASS_NAME, "locality").text
            except:
                address2 = ""

            full_address = f"{address1}, {address2}".strip(", ")

            results.append({
                "Name": name,
                "Phone": phone,
                "Address": full_address
            })

finally:
    driver.quit()
    df = pd.DataFrame(results)
    df.to_excel("leads.xlsx", index=False)
    print(f"✅ Scraping complete! {len(results)} leads saved to leads.xlsx")
