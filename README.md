# Perfume Image Downloader

## Overview

This project is a Python script that downloads images of perfumes from Fragrantica based on a provided CSV file containing perfume names and their corresponding URLs. The images are saved in dedicated folders named after each perfume, with a specific naming convention.

## Features

- Downloads images from Fragrantica for each perfume listed in a CSV file.
- Creates a dedicated folder for each perfume, named in the format `Perfume_Name | Perfume_Alternate_Name`.
- Implements a random wait time between requests to avoid overwhelming the server (between 2 to 5 minutes).
- Uses BeautifulSoup for web scraping to extract image URLs.
- Provides console logs to track progress and any errors encountered.

## Requirements

- Python 3.6 or higher
- Required libraries:
  - `requests`
  - `beautifulsoup4`
  - `tqdm`

## Installation

1. Clone the repository or download the script:
   ```bash
   git clone <repository_url>
   cd perfume-image-downloader
   ```

2. Install the required libraries:
   ```bash
   pip install requests beautifulsoup4 tqdm
   ```

3. Prepare a CSV file named `name_url.csv` in the same directory, structured as follows:
   ```csv
   name_in_website,url
   "Perfume Name 1","http://fragrantica.com/perfume-url-1"
   "Perfume Name 2","http://fragrantica.com/perfume-url-2"
   ```

## Usage

To run the script, execute the following command in your terminal:
```bash
python perfume_image_downloader.py
```

The script will read the `name_url.csv` file, download the images from the specified URLs, and save them in dedicated folders.

## Folder Structure

The images will be saved in a directory called `perfume_images`. Each perfume will have its own folder, named in the format:
```
Perfume_Name | Perfume_Alternate_Name
```

## Logging

The script provides detailed logging to the console, indicating the progress of image downloads and any errors encountered.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.
