import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

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

def get_episode_links(playlist_url, driver):
    """Extract all episode links from a Spotify playlist."""
    driver.get(playlist_url)
    time.sleep(5)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    episode_links = []
    episodes = driver.find_elements(By.XPATH, '//a[contains(@href, "/episode/")]')
    for episode in episodes:
        link = episode.get_attribute("href")
        if link and link not in episode_links:
            episode_links.append(link)

    return episode_links

def scrape_episode_data(episode_url, driver):
    """Scrape podcast episode details (title, duration, and link)."""
    driver.get(episode_url)
    time.sleep(3)

    try:
        title_element = driver.find_element(By.TAG_NAME, "h1")
        title = title_element.text.strip()
    except:
        title = "Title Not Found"

    try:
        duration_element = driver.find_element(By.XPATH, '//span[contains(text(), "min") or contains(text(), "sec")]')
        duration = duration_element.text.strip()
    except:
        duration = "Duration Not Found"

    return {
        "Title": title,
        "Duration": duration,
        "Link": episode_url
    }


def save_to_json(data, filename="spotify_podcasts.json"):
    """Save the scraped data to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main(playlist_url):
    """Main function to scrape all episodes from a Spotify playlist."""
    driver = setup_driver()
    
    print("[*] Collecting episode links...")
    episode_links = get_episode_links(playlist_url, driver)
    
    print(f"[*] Found {len(episode_links)} episodes. Scraping details...")
    all_episodes = []

    for idx, episode_url in enumerate(episode_links):
        print(f"[*] Scraping episode {idx + 1}/{len(episode_links)}")
        episode_data = scrape_episode_data(episode_url, driver)
        all_episodes.append(episode_data)

    driver.quit()

    save_to_json(all_episodes)
    print("[✓] Data saved to 'spotify_podcasts.json'")

playlist_url = "https://open.spotify.com/playlist/6fxh57iMU4NYxI41mfD0cV"
main(playlist_url)
