import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import json

parser = argparse.ArgumentParser(description="Web Scraper with Depth")
parser.add_argument("--start_url", required=True, help="The starting URL for web scraping")
parser.add_argument("--domain", required=True, help="The domain to restrict web scraping")
parser.add_argument("--max_depth", type=int, default=1, help="Maximum depth for web scraping")
args = parser.parse_args()

start_url = args.start_url
domain = args.domain
max_depth = args.max_depth

folder_path = f"data/{domain}"
if os.path.exists(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            os.rmdir(dir_path)
    os.rmdir(folder_path)

os.makedirs(folder_path)

def write_html_to_txt(url, data):
    print(f"saving for {url}")
    url = url.replace(":", "_").replace("/", "_")
    file_name = f"{url}.html"
    file_path = os.path.join(folder_path, file_name)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)
    else:
        print(f"warning: already exists!")

def is_same_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == domain

def is_valid_url(url):
    return "#" not in url

def scrape_links(url, depth):
    if depth > max_depth:
        return []
    # print(f"Scraping links from: {url}, Depth: {depth}")
    links = []
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        soup = BeautifulSoup(response.content, "html.parser")
        write_html_to_txt(url, response.text)
        links.append(url)

        with ThreadPoolExecutor(max_workers=5) as executor:
            link_futures = []
            for link in soup.find_all("a"):
                href = link.get("href")
                if href and is_valid_url(href):
                    absolute_url = urljoin(url, href)
                    if absolute_url.startswith("/") or (is_same_domain(absolute_url) and absolute_url.startswith("https://")):
                        link_futures.append(executor.submit(scrape_links, absolute_url, depth + 1))
            for future in link_futures:
                links.extend(future.result())
    except Exception as e:
        print(f"An error occurred while scraping {url}: {str(e)}")
    
    return links

def scrape_all_links(url, depth=0):
    if depth > max_depth:
        return set()

    visited = set()
    to_visit = [(url, depth)]

    start_time = time.time()

    while to_visit:
        print("*" * 100)
        print(f"{len(to_visit)} <- queue")
        print(f"already visited: {len(visited)}")
        print("*" * 100)
        current_url, current_depth = to_visit.pop(0)
        if current_url not in visited:
            visited.add(current_url)
            print(f"Visiting: {current_url}, Depth: {current_depth}")
            links = scrape_links(current_url, current_depth)
            add_links = [(url, depth) for url in links if url not in visited]
            print(f"adding {len(add_links)} to the queue")
            to_visit.extend(add_links)

    end_time = time.time()
    elapsed_time_minutes = (end_time - start_time) / 60
    print(f"Total time taken: {elapsed_time_minutes:.2f} minutes")

    file_path = os.path.join(folder_path, "visited.json")
    with open(file_path, "w", encoding="utf-8") as file:
        visited_list = list(visited)
        json.dump(visited_list, file, indent=2)

    return visited

all_links = scrape_all_links(start_url)
