from langchain.llms import Ollama
import time

def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time:.4f} seconds to execute.")
        return result
    return wrapper

@timeit
def run():
    html_path = '/Users/architsingh/Documents/projects/auto-scraper/data/react.dev/https___react.dev_learn.txt'
    with open(html_path, 'r') as f:
        html_data = f.read()
    
    llm = Ollama(model="mistral-openorca")
    query=f"extract the blog from this html in clean fashion: {html_data}"
    print(len(query))
    
    res = llm.predict(query)
    print(len(res))
    print(res)

if __name__ == "__main__":
    run()
