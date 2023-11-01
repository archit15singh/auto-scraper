import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain.llms import Ollama
from langchain.document_loaders import WebBaseLoader
from langchain.chains.summarize import load_summarize_chain

base_url = 'https://ollama.ai/blog'

visited_links = set()

def scrape_links(url, visited_links):
    scraped_links = []
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    absolute_url = urljoin(url, href)
                    
                    if absolute_url.startswith(base_url) and absolute_url not in visited_links:
                        scraped_links.append(absolute_url)
                        visited_links.add(absolute_url)
                        scraped_links.extend(scrape_links(absolute_url, visited_links))
    except Exception as e:
        print(f"Error: {str(e)}")
    
    return scraped_links

start_url = base_url
all_scraped_links = scrape_links(start_url, visited_links)
print(len(all_scraped_links))

for scraped_link in all_scraped_links:
    print(scraped_link)
    loader = WebBaseLoader(scraped_link)
    docs = loader.load()
    print(len(docs[0].page_content))

    llm = Ollama(model="llama2")
    chain = load_summarize_chain(llm, chain_type="stuff")
    result = chain.run(docs)
    print(f"len of result {len(result)}")
