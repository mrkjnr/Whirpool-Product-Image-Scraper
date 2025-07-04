import os
import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def scrape_images_from_csv(csv_path):
    IMAGE_DIR = 'static/whirlpool_images'  # Folder where images will be saved
    os.makedirs(IMAGE_DIR, exist_ok=True)  # Create image folder if it doesn't exist

    # Setup headless Chrome options for silent scraping
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    # Setup image downloader with retry logic
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    total_scraped = 0  # Count of successfully scraped products

    # Open and read the CSV file
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, start=2):
            part_number = row.get("Title", "").strip()
            product_url = row.get("PRODUCT URL", "").strip()

            if not part_number or not product_url:
                continue  # Skip rows with missing data

            try:
                print(f"[{i}] Scraping images for: {part_number} — {product_url}")
                driver.get(product_url)
                time.sleep(2)  # Wait for the page to load

                images = driver.find_elements(By.TAG_NAME, "img")
                seen_urls = set()
                image_count = 0

                for index, img in enumerate(images):
                    img_url = img.get_attribute("src")
                    if not img_url:
                        continue

                    # Skip unwanted images (logos, placeholders, icons)
                    skip_keywords = ['logo', 'placeholder', 'spinner', 'icon']
                    if any(k in img_url.lower() for k in skip_keywords):
                        continue

                    # Avoid duplicates
                    if img_url in seen_urls:
                        continue
                    seen_urls.add(img_url)

                    try:
                        image_data = session.get(img_url).content
                        filename = os.path.join(IMAGE_DIR, f"{part_number}_{image_count}.jpg")
                        with open(filename, 'wb') as f_img:
                            f_img.write(image_data)
                        image_count += 1
                    except Exception as e:
                        print(f"⚠️ Failed to download image {img_url}: {e}")

                if image_count == 0:
                    print(f"⚠️ No valid images found for {part_number}")
                else:
                    total_scraped += 1

            except Exception as e:
                print(f"❌ Error scraping {part_number} (Row {i}): {e}")
                continue

    driver.quit()
    print(f"\n✅ Done! Scraped images for {total_scraped} part(s).\n")

# Example usage:
# scrape_images_from_csv("input.csv")