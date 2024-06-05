import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the article title
        title = soup.find('h1').get_text() if soup.find('h1') else 'No title found'

        # Extract the article content
        paragraphs = soup.find_all('p')
        content = '\n'.join([para.get_text() for para in paragraphs])

        return title, content

    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None, None

# URL of the article to scrape
article_url = 'https://techcrunch.com/2024/06/03/binit-is-bringing-ai-to-trash/'
title, content = scrape_article(article_url)

if title and content:
    print("Article Title:", title)
    print("Article Content:", content)
