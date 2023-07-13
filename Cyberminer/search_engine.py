import requests
from bs4 import BeautifulSoup

class GoogleSearcher:
    def __init__(self):
        self.GOOGLE_SEARCH_URL = "https://google.com/search"

    def google_search(self, query):
        result = requests.get(self.GOOGLE_SEARCH_URL, params={'q': query})
        soup = BeautifulSoup(result.text, "html.parser")
        return [a['href'] for a in soup.find_all('a')]

# Usage:
# gs = GoogleSearcher()
# results = gs.google_search('Python')
# print(results)
