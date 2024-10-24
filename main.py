import os
import requests
import csv
import time
import random
from bs4 import BeautifulSoup
from tqdm import tqdm

# Download images of the given perfume
def download_images(perfume_name, perfume_url):
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        print(f"Accessing {perfume_name} at {perfume_url}...")
        response = requests.get(perfume_url, headers=headers, timeout=15)
        response.raise_for_status()
        print(f"Successfully accessed {perfume_name} page.")

        soup = BeautifulSoup(response.text, 'html.parser')
        fragram_photos_wrapper = soup.find('fragram-photos-wrapper')

        if not fragram_photos_wrapper:
            print(f"No 'fragram photos' section found on the page for {perfume_name}.")
            return False

        image_tags = fragram_photos_wrapper.find_all('div', class_='carousel-cell-photo')
        if not image_tags:
            print(f"No image tags found for {perfume_name}. Please check the HTML structure.")
            return False

        # Create a folder for the perfume images with spaces instead of underscores
        folder_name = f"perfume_images/{perfume_name} | {perfume_name.split('|')[-1].strip()}"
        create_folder(folder_name)

        for img_tag in image_tags:
            a_tag = img_tag.find('a', itemprop='image')
            if a_tag and 'href' in a_tag.attrs:
                img_url = a_tag['href']
                image_name = os.path.basename(img_url)

                print(f"Downloading image: {image_name} from {img_url}...")
                img_response = requests.get(img_url, headers=headers, timeout=15)
                img_response.raise_for_status()

                image_path = os.path.join(folder_name, image_name)
                with open(image_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"Downloaded {perfume_name} image to {image_path}.")
            else:
                print(f"No image found in the anchor tag for {perfume_name}.")

        return True

    except requests.exceptions.HTTPError as e:
        print(f"Failed to retrieve {perfume_name} page. HTTPError: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {perfume_name}. Error: {e}")
        return False

# Create a directory for perfume images if it doesn't exist
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created directory: {folder_name}")
    else:
        print(f"Directory already exists: {folder_name}")

# Download images from the provided CSV file
def download_images_from_csv(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        perfumes = [row for row in reader]

    print(f"Starting to download images for {len(perfumes)} perfumes...")

    for perfume in tqdm(perfumes, desc="Downloading images"):
        perfume_name = perfume['name_in_website']
        perfume_url = perfume['url']

        # Download images for each perfume
        if not download_images(perfume_name, perfume_url):
            print(f"Failed to download images for {perfume_name}.")

        # Wait for a random time between 2 to 5 minutes before the next request
        wait_time = random.uniform(120, 300)  # Random wait time between 120 seconds (2 minutes) and 300 seconds (5 minutes)
        print(f"Waiting for {wait_time:.2f} seconds before the next download...")
        time.sleep(wait_time)

if __name__ == "__main__":
    csv_file = 'name_url.csv'  # Update with your CSV filename
    download_images_from_csv(csv_file)
