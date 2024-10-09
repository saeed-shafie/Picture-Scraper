import os
import requests
import csv
import random
from bs4 import BeautifulSoup
from tqdm import tqdm

# Sample user agents for web requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    # Add more user agents as needed
]

# Load proxies from the given file
def load_proxies(proxy_file):
    proxies = []
    with open(proxy_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            proxy_url = row['proxy']  # Assuming the proxy URL is in the 'proxy' column
            proxies.append(proxy_url)
    return proxies

# Test if proxies are working and attempt to download images if successful
def test_proxies_and_download_images(proxies, perfume_name, perfume_url):
    for proxy in proxies:
        proxy_type = 'http' if proxy.startswith('http://') else 'https'
        try:
            print(f"Testing proxy: {proxy}")
            response = requests.get('http://httpbin.org/ip', proxies={proxy_type: proxy}, timeout=10)  # Increased timeout
            if response.status_code == 200:
                print(f"Working proxy: {proxy}")

                # If the proxy is working, attempt to download images for the given perfume
                if download_images(perfume_name, perfume_url, proxy):
                    print(f"Successfully downloaded images for {perfume_name} using proxy {proxy}.")
                    return True  # Exit on successful download
                else:
                    print(f"Failed to download images for {perfume_name} with proxy {proxy}.")
            else:
                print(f"Proxy failed with status code: {response.status_code} - {proxy}")
        except requests.exceptions.RequestException as e:
            print(f"Proxy error: {e} - {proxy}")

    return False  # If no working proxies could download images successfully

# Download images of the given perfume
def download_images(perfume_name, perfume_url, proxy):
    user_agent = random.choice(USER_AGENTS)
    headers = {'User-Agent': user_agent}
    proxies = {'http': proxy, 'https': proxy}

    try:
        print(f"Accessing {perfume_name} at {perfume_url} using proxy {proxy} and user agent {user_agent}...")
        response = requests.get(perfume_url, headers=headers, proxies=proxies, timeout=15, verify=False)  # Increased timeout and disabled SSL verification for testing
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        fragram_photos_wrapper = soup.find('fragram-photos-wrapper')

        if not fragram_photos_wrapper:
            print(f"No fragram photos section found on the page for {perfume_name}.")
            return False

        image_tags = fragram_photos_wrapper.find_all('div', class_='carousel-cell-photo')
        if not image_tags:
            print(f"No image tags found for {perfume_name}. Check the HTML structure.")
            return False

        folder_name = f"perfume_images/{perfume_name.replace(' ', '_')}"
        create_folder(folder_name)

        for img_tag in image_tags:
            a_tag = img_tag.find('a', itemprop='image')
            if a_tag and 'href' in a_tag.attrs:
                img_url = a_tag['href']
                image_name = os.path.basename(img_url)

                img_response = requests.get(img_url, headers=headers, proxies=proxies, timeout=15, verify=False)  # Increased timeout and disabled SSL verification for testing
                img_response.raise_for_status()

                image_path = os.path.join(folder_name, image_name)
                with open(image_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"Downloaded {perfume_name} image to {image_path}")
            else:
                print(f"No image found in a tag for {perfume_name}.")

        return True

    except requests.exceptions.HTTPError as e:
        print(f"Failed to retrieve {perfume_name} page. HTTPError: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {perfume_name} with proxy {proxy}. Error: {e}")
        return False

# Create a directory for perfume images if it doesn't exist
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created directory: {folder_name}")

# Download images from the provided CSV file, using one proxy at a time
def download_images_from_csv(csv_file, proxies):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        perfumes = [row for row in reader]

    for perfume in tqdm(perfumes, desc="Downloading images"):
        perfume_name = perfume['name_in_website']
        perfume_url = perfume['url']

        # Test proxies and download images for each perfume
        if not test_proxies_and_download_images(proxies, perfume_name, perfume_url):
            print(f"Failed to download images for {perfume_name} with all tested proxies.")

if __name__ == "__main__":
    csv_file = 'name_url.csv'  # Update with your CSV filename
    proxy_file = 'proxies.txt'  # Update with your proxy filename

    # Load and test proxies
    proxy_list = load_proxies(proxy_file)

    if proxy_list:
        print("Using the following proxies for scraping:")
        download_images_from_csv(csv_file, proxy_list)
    else:
        print("No proxies available. Please check your proxy list.")
