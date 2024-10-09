# 🥀 Perfume Image Scraper

Welcome to the **Perfume Image Scraper**! 🌟 This tool allows fragrance enthusiasts to download user-uploaded pictures of perfumes from the Fragrantica website.

## 📚 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Proxy Management](#proxy-management)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Download Images**: Easily download images from Fragrantica. 📸
- **User-Agent Rotation**: Mimic different browsers. 🦾
- **Proxy Support**: Bypass restrictions. 🔒
- **CSV Input**: Load perfume names and URLs. 📄
- **Progress Tracking**: Monitor your downloads. ⏳

## 🛠 Requirements

- Python packages: `requests`, `beautifulsoup4`, `tqdm`.

Install them with:

```bash
pip install requests beautifulsoup4 tqdm
```

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/perfume-image-scraper.git
   cd perfume-image-scraper
   ```

2. Place your `name_url.csv` and `proxies.txt` in the directory.

## 📝 Usage

1. Update the script with your CSV and proxy filenames:

   ```python
   csv_file = 'name_url.csv'
   proxy_file = 'proxies.txt'
   ```

2. Run the scraper:

   ```bash
   python perfume_scraper.py
   ```

Images will be saved in the `perfume_images` directory. 🗂️

## 🔍 How It Works

1. **Load Proxies**: Reads the proxy list.
2. **Test Proxies**: Validates each proxy.
3. **Scrape Images**: Fetches image URLs.
4. **Download Images**: Saves images organized by perfume name.

## 🌐 Proxy Management

Use reliable proxies in `proxies.txt`:

```
http://proxy1:port
http://proxy2:port
https://proxy3:port
```

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository. 🍴
2. Create a branch. 🌳
3. Push changes and submit a pull request. 📥

## 📜 License

This project is licensed under the MIT License. Feel free to use and modify it.

---

Thank you for using the **Perfume Image Scraper**! Happy scraping! 🎉
```
