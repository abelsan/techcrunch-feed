import feedparser
import requests
from bs4 import BeautifulSoup
import json

def create_filename(text, max_length=50):
    # Remove any characters that are not allowed in file names
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        text = text.replace(char, '')
    
    # Replace spaces with underscores
    text = text.replace(' ', '_')
    
    # Truncate the text to the maximum length
    if len(text) > max_length:
        text = text[:max_length]
    
    # Add file extension
    filename = f"{text}.txt"
    
    return filename

def scrape_article(url, filename):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the article title
        title = soup.find('h1').get_text() if soup.find('h1') else 'No title found'

        # Select the "entry-content" div
        entry_content_div = soup.find('div', class_='entry-content')

        # Extract all paragraphs with the class "wp-block-paragraph" from the "entry-content" div
        paragraphs = entry_content_div.find_all('p', class_='wp-block-paragraph')

        # join the paragraphs to form the content                
        content_no_newlines = '<NEWLINE>'.join([para.get_text() for para in paragraphs])
        content = '\n\n'.join([para.get_text() for para in paragraphs])
   
        if title and content:
            # Open the file in write mode to write the first content
            with open("data/"+filename, 'w') as file:
                file.write("Article Title: " + title + "\n")

            # Open the same file in append mode to write the second content
            with open("data/"+filename, 'a') as file:
                file.write("Article Content: " + content)    

        return content_no_newlines

    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None, None


def parse_rss_feed(url):
    # Parse the RSS feed
    feed = feedparser.parse(url)

    # Check for bozo flag to detect feed parsing errors
    if feed.bozo:
        raise Exception("Error parsing feed: {}".format(feed.bozo_exception))

    # Prepare a list to store the feed entries
    feed_entries = []

    # Loop through the feed entries and collect the required data
    for entry in feed.entries:
        filename = create_filename(entry.title)
        content = scrape_article(entry.link, filename)
        print(f"Processing article: {entry.title}")
        entry_data = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary,
            'content': content
        }
        feed_entries.append(entry_data)

    return feed_entries

def save_to_json(data, filename):
    # Write the data to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# URL of the RSS feed
rss_url = 'https://techcrunch.com/category/artificial-intelligence/feed/'

# Parse the RSS feed and get the entries
feed_entries = parse_rss_feed(rss_url)

# Save the entries to a JSON file
save_to_json(feed_entries, 'rss_feed_entries.json')
