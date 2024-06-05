import feedparser
import json

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
        entry_data = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary
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
