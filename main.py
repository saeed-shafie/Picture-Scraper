import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to create a folder if it doesn't exist
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Function to download images from the Loewe 7 perfume page
def download_images(perfume_name, perfume_url):
    # Set headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    # Make HTTP request to the page
    response = requests.get(perfume_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve {perfume_name} page. Status code: {response.status_code}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the fragram photos section
    fragram_photos_wrapper = soup.find('fragram-photos-wrapper')
    if not fragram_photos_wrapper:
        print(f"No fragram photos section found on the page for {perfume_name}.")
        return

    # Find all carousel cell photos
    image_tags = fragram_photos_wrapper.find_all('div', class_='carousel-cell-photo')

    # Create a folder for the perfume
    folder_name = f"perfume_images/{perfume_name.replace(' ', '_')}"
    create_folder(folder_name)

    # Loop through the image tags and download each image
    for img_tag in image_tags:
        a_tag = img_tag.find('a', itemprop='image')
        if a_tag and 'href' in a_tag.attrs:
            img_url = a_tag['href']  # Use the href for high-quality image
            image_name = os.path.basename(img_url)  # Get the image name from URL

            # Use requests to download the image
            try:
                img_response = requests.get(img_url, headers=headers)
                img_response.raise_for_status()  # Check for request errors

                # Save the image
                image_path = os.path.join(folder_name, image_name)
                with open(image_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"Downloaded {perfume_name} image to {image_path}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download image from {img_url}. Error: {e}")
        else:
            print(f"No image found in a tag for {perfume_name}.")

# Testing the function with Loewe 7 Loewe
perfume_name = "Loewe 7 Loewe"
perfume_url = "https://www.fragrantica.com/perfume/Loewe/Loewe-7-10253.html"

download_images(perfume_name, perfume_url)
