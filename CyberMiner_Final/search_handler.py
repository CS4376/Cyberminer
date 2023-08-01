from googlesearch import search
import datetime
import requests
from htmldate import find_date
from bs4 import BeautifulSoup

class GoogleSearcher:
    def __init__(self):
        self.case_sensitive = False
        self.search_mode = 'OR'
        self.symbols = []
        self.keyword = ''
        self.results = []

    def filter_symbols(self, query):
        return ''.join(i for i in query if not i in self.symbols)

    def search_google(self, keyword, count, expiry_date, min_year, sortOrder, search_mode='OR'):
        # Convert the expiry_date from a string to a datetime object
        expiry_date = datetime.datetime.fromisoformat(expiry_date) if expiry_date else None

        if search_mode == 'AND':
            query = ' AND '.join(keyword.split())
        elif search_mode == 'NOT':
            query = keyword.replace(' ', ' -')
        elif search_mode == 'OR':
            query = ' OR '.join(keyword.split())

        query = self.filter_symbols(query)

        results = set()
        for url in search(query, num_results=count):
            last_published_date_str = self.get_last_published_date(url)
            # Convert the last_published_date from a string to a datetime object
            last_published_date = datetime.datetime.fromisoformat(last_published_date_str) if last_published_date_str else None
            # If an expiry_date was provided, only include the result if it was published after the expiry_date
            # If a min_year was provided, only include the result if it was published after the beginning of the min_year
            if (not expiry_date or (last_published_date and last_published_date > expiry_date)) and (not min_year or (last_published_date and last_published_date.year >= min_year)):
                results.add(url)
                if len(results) == count:
                    break

        timestamp = datetime.datetime.now().isoformat()
        new_results = [{'keyword': keyword, 'title': self.get_website_title(url), 'url': url, 'timestamp': timestamp, 'last_published_date': self.get_last_published_date(url)} for url in results]

        if sortOrder == "asc":
            new_results.sort(key=lambda x: x['title'].lower())
        elif sortOrder == "dsc":
            new_results.sort(key=lambda x: x['title'].lower(), reverse=True)
        elif sortOrder == "freq":
            # Example: sort by frequency of a particular word or pattern
            new_results.sort(key=lambda x: x['title'].lower().count('your_word_here'))
        elif sortOrder == "payment":
            # Example: sort by whether a payment is required, assuming 'payment_required' field exists
            new_results.sort(key=lambda x: x['payment_required'])


        self.results.extend(new_results)
        self.clean_outdated_results()  # delete outdated urls
        return new_results

    def get_website_title(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').text.strip()
        return title

    def get_last_published_date(self, url):
        try:
            response = requests.get(url)
            html_content = response.content.decode('utf-8')
            published_date = find_date(html_content)
            return published_date
        except Exception as e:
            print(f"Error while getting last published date for URL '{url}': {e}")
            return None

    def clean_outdated_results(self):
        one_year_ago = (datetime.datetime.now() - datetime.timedelta(days=365)).isoformat()
        self.results = [result for result in self.results if result['last_published_date'] and result['last_published_date'] >= one_year_ago]