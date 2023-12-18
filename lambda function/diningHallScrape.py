import requests
from bs4 import BeautifulSoup
import re
import json
import boto3
import os
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('diningHall')

def scrape_menu(url, script_index):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; en-US) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/54.0.1370.133 Safari/602'}
    response = requests.get(url, headers=headers)

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
                return menu_data
            else:
                print(f"No match found in script for {url}")
        else:
            print(f"Script index {script_index} out of range for {url}")
    else:
        print(f"Failed to retrieve data from {url}")
    return None

def lambda_handler(event, context):
    current_date = datetime.now().strftime('%Y-%m-%d')

    urls = [
        ('https://dining.columbia.edu/content/john-jay-dining-hall', 10),
        ('https://dining.columbia.edu/content/ferris-booth-commons-0', 11),
        ('https://dining.columbia.edu/content/jjs-place-0', 10)
    ]

    for url, index in urls:
        menu_data = scrape_menu(url, index)
        if menu_data:
            # Update DynamoDB with the scraped data
            response = table.put_item(Item={
                'url': url,
                'date': current_date,
                'menu_data': menu_data
            })
            print(f"DynamoDB update response for {url}: {response}")
        else:
            print(f"No data to update for {url}")

    return {
        'statusCode': 200,
        'body': 'Data scraping and update completed successfully'
    }