import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime

def fetch_static_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to retrieve the webpage")
        return None

def fetch_dynamic_page(url):
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
    driver.get(url)
    time.sleep(5)  # Adjust based on the page's load time
    html_content = driver.page_source
    driver.quit()
    return html_content

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')
    text_content = "\n".join([p.get_text() for p in paragraphs])
    return text_content

def get_desktop_path():
    return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

def generate_filename():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"scraped_content_{timestamp}.txt"

def save_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Text saved to {file_path}")

def read_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def main():
    url = input("Enter the URL of the webpage to scrape: ")
    desktop_path = get_desktop_path()
    filename = generate_filename()
    file_path = os.path.join(desktop_path, filename)

    # Choose between static and dynamic page fetching
    is_dynamic = input("Is this a dynamic webpage? (yes/no): ").strip().lower() == 'yes'
    
    if is_dynamic:
        html_content = fetch_dynamic_page(url)
    else:
        html_content = fetch_static_page(url)
    
    if html_content:
        text_content = parse_html(html_content)
        save_to_file(text_content, file_path)
        saved_text = read_from_file(file_path)
        print("\n--- Saved Text ---\n")
        print(saved_text)

if __name__ == "__main__":
    main()
