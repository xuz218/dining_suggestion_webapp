import requests
from bs4 import BeautifulSoup
import re
import json

def scrape_menu(url, script_index):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; en-US) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/54.0.1370.133 Safari/602'}
    response = requests.get(url, headers=headers)
    print(f"Status Code for {url}: {response.status_code}")  # Check if the request was successful

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        script_tags = soup.find_all('script')
        if script_index < len(script_tags):
            script = script_tags[script_index]
            pattern = r'var menu_data = `(.+)`;'
            match = re.search(pattern, script.text)
            if match:
                json_data = match.group(1)
                json_string = json_data.replace("\\", "")
                menu_data = json.loads(json_string)
                json_object = json.dumps(menu_data, indent=4)
                with open(f"{url.split('/')[-1]}.json", "w") as outfile:
                    outfile.write(json_object)
                print(f"File written for {url}")
            else:
                print(f"No match found in script for {url}")
        else:
            print(f"Script index {script_index} out of range for {url}")
    else:
        print(f"Failed to retrieve data from {url}")

# URLs and their respective script indexes
urls = [
    ('https://dining.columbia.edu/content/john-jay-dining-hall', 10),
    ('https://dining.columbia.edu/content/ferris-booth-commons-0', 11),
    ('https://dining.columbia.edu/content/jjs-place-0', 10)
]

for url, index in urls:
    scrape_menu(url, index)
