# Internship Scraper

This project scrapes internship offers from Thomas More's internships portal and saves them to a json file for further analysis or processing.

## Features

-   Scrape internships using Selenium

## Usage

### 1. Scrape Internships

```bash
python main.py
```

This will save all internships to `output/internships.json`.

## Requirements

-   Python 3.8+
-   ChromeDriver (for Selenium)

Install dependencies:

```bash
pip install selenium
```

## Configuration

-   Before running the script, make sure to add `cookies.json`. This file should contain the cookies needed to access the internships portal. You can obtain this file by logging into the portal and exporting the cookies using your browser's developer tools.

-   Make sure to have the correct version of ChromeDriver installed that matches your Chrome browser version.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE VERSION 2. See the [LICENSE](LICENSE) file for details.
