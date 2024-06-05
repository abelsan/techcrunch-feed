import feedparser

def parse_rss_feed(url):
    try:
        # Parse the RSS feed
        feed = feedparser.parse(url)

        # Check for bozo flag to detect feed parsing errors
        if feed.bozo:
            raise Exception("Error parsing feed: {}".format(feed.bozo_exception))

        # Print feed title
        print("Feed Title:", feed.feed.title)

        # Loop through the feed entries and print the title of each entry
        for entry in feed.entries:
            print("Entry Title:", entry.title)
            print("Entry Link:", entry.link)
            print("Entry Published Date:", entry.published)
            print("Entry Summary:", entry.summary)
            print("------------")
    except Exception as e:
        print("Failed to parse RSS feed:", str(e))

# URL of the RSS feed
rss_url = 'https://techcrunch.com/category/artificial-intelligence/feed/'
parse_rss_feed(rss_url)
