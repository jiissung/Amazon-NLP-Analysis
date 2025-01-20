import requests
from bs4 import BeautifulSoup
"""
Scrapes Amazon Reviews present on Amazon Product's Page
"""

class AmazonScraper:
    def __init__(self, url):
        # creates the url and the machine header to scrape
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

    def get_data(self):
        """
        Sends a request and gets the response html
        """
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from URL: {e}")
            return None

    def parse_html(self):
        """
        Parses through the html and returns a beautiful soup object
        """
        htmldata = self.get_data()
        return BeautifulSoup(htmldata, 'html.parser')


    def extract_reviews(self):
        """
        Extracts product reviews from soup HTML
        """
        soup = self.parse_html()
        reviews = []
        for review_div in soup.find_all("div", {"data-hook": "review-collapsed"}):
            span = review_div.find("span")
            if span:
                reviews.append(span.text.strip())
        return reviews

    @staticmethod
    def clean_reviews(reviews):
        """
        removes empty strips
        """
        return [review for review in reviews if review.strip()]



