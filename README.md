# Web Scraper with Depth

This Python script allows you to perform web scraping with a specified maximum depth. It provides a flexible and easy-to-use command-line interface to scrape web pages from a given starting URL within a specified domain while adhering to the maximum depth constraint.

## Features

- Web scraping with a defined maximum depth.
- Ability to specify the starting URL and domain for scraping.
- Organizes scraped HTML content in text files.
- Command-line interface for ease of use.
- Prevents scraping external or irrelevant URLs.

## Prerequisites

Before using the script, ensure you have Python installed on your system. Additionally, install the required Python libraries using the following command:

```bash
pip install requests beautifulsoup4
```

## Usage

1. Clone or download this repository to your local machine.

2. Open your terminal or command prompt and navigate to the script's directory.

3. Use the following command to execute the script:

```bash
python web_scraper.py --start_url <start_url> --domain <domain> --max_depth <max_depth>
```

Replace the placeholders with your desired values:

- `<start_url>`: The starting URL for web scraping.
- `<domain>`: The domain to restrict web scraping.
- `<max_depth>`: The maximum depth for web scraping.

For example, to scrape pages starting from "https://example.com" with a maximum depth of 2 within the "example.com" domain, use:

```bash
python web_scraper.py --start_url https://example.com --domain example.com --max_depth 2
```

## Output

The script will create a folder named after the specified domain to store the scraped HTML content. Each HTML page is saved in a separate text file with a unique identifier as the filename.

## Contributing

If you'd like to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.