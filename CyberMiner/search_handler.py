from googlesearch import search
import datetime
import requests
from htmldate import find_date

class GoogleSearcher:
    def __init__(self):
        self.case_sensitive = False
        self.search_mode = 'OR'
        self.symbols = []
        self.keyword = ''
        self.results = []

    def filter_symbols(self, query):
        return ''.join(i for i in query if not i in self.symbols)

    def search_google(self, keyword, count, offset=0):
        query = self.search_mode.join(keyword.split()) if self.search_mode in ['AND', 'OR'] else keyword.replace('NOT', '-')
        query = self.filter_symbols(query)

        results = []
        for result in search(query, num_results=count + offset):
            results.append(result)
            if len(results) == count + offset:
                break

        # Only return the required results for the current page
        results = results[offset:]

        timestamp = datetime.datetime.now().isoformat()
        self.results = [{'keyword': keyword, 'url': url, 'timestamp': timestamp, 'last_published_date': self.get_last_published_date(url)} for url in results]
        return self.results

    def get_last_published_date(self, url):
        try:
            response = requests.get(url)
            html_content = response.content.decode('utf-8')
            published_date = find_date(html_content)
            return published_date
        except Exception as e:
            print(f"Error while getting last published date for URL '{url}': {e}")
            return None
