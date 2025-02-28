import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def setup_driver():
    """Set up Selenium WebDriver."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def close_cookie_popup(driver):
    """Close the cookie consent popup if it appears."""
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))
        )
        allow_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
        allow_button.click()
        print("[✓] Cookie consent dismissed.")
        time.sleep(2)
    except Exception:
        print("[⚠] No cookie pop-up found or already dismissed.")

def scrape_page(driver):
    """Scrape blog data from the current page."""
    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = []

    blog_cards = soup.find_all("article", class_="m05_blog_three_col-item")

    for card in blog_cards:
        try:
            title = card.find("h5").text.strip()
        except AttributeError:
            title = "No Title"

        try:
            tag = card.find("div", class_="blog-tag").text.strip()
        except AttributeError:
            tag = "No Tag"

        try:
            link = card.find("a", class_="gtm-linkclick")["href"]
            if not link.startswith("http"):
                link = "https://www.irishlifehealth.ie" + link
        except AttributeError:
            link = "No Link"

        try:
            img_tag = card.find("img")
            img_url = img_tag["src"] if img_tag else "No Image"
            if not img_url.startswith("http"):
                img_url = "https://www.irishlifehealth.ie" + img_url
        except AttributeError:
            img_url = "No Image"

        articles.append({
            "Title": title,
            "Tag": tag,
            "Link": link,
            "Image": img_url
        })

    print(f"[✓] Found {len(articles)} articles on this page.")
    return articles

def save_to_json(data, filename="irishlife_blog.json"):
    """Save scraped data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def click_pagination_number(driver, page_number):
    """Click a pagination number."""
    try:
        page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, str(page_number)))
        )

        driver.execute_script("arguments[0].scrollIntoView();", page_button)
        time.sleep(1)
        page_button.click()
        print(f"[✓] Clicked on Page {page_number}")
        time.sleep(3)

    except Exception as e:
        print(f"[!] Failed to click page {page_number}: {e}")

def main():
    """Main function to scrape 3 pages of the Irish Life blog."""
    driver = setup_driver()
    url = "https://www.irishlifehealth.ie/blog"
    driver.get(url)
    time.sleep(3)

    close_cookie_popup(driver)

    all_articles = []

    for page in range(1, 4):
        print(f"[*] Scraping Page {page}...")
        all_articles.extend(scrape_page(driver))

        if page < 3:
            click_pagination_number(driver, page + 1)

    driver.quit()

    save_to_json(all_articles)
    print("[✓] Data saved to 'irishlife_blog.json'")

if __name__ == "__main__":
    main()
