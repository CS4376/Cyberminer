from googlesearch import search
import sys
import webbrowser
import sqlite3
import datetime
import requests
from bs4 import BeautifulSoup
from htmldate import find_date
from flask import Flask, request, jsonify

app = Flask(__name__)

class GoogleSearcher:
    def __init__(self):
        self.case_sensitive = False
        self.search_mode = 'OR'
        self.symbols = []
        self.keyword = ''
        self.results = []

    def filter_symbols(self, query):
        return ''.join(i for i in query if not i in self.symbols)

    def _search_google(self, keyword, count):
        query = self.search_mode.join(keyword.split()) if self.search_mode in ['AND', 'OR'] else keyword.replace('NOT', '-')
        query = self.filter_symbols(query)

        connection = sqlite3.connect('search_results.db')
        cursor = connection.cursor()

        results = []
        for result in search(query, stop=count):
            results.append(result)
            if len(results) == count:
                break

        timestamp = datetime.datetime.now().isoformat()
        self.results = [(keyword, url, timestamp, self.get_last_published_date(url)) for url in results]
        for result in self.results:
            cursor.execute('INSERT INTO search_results (keyword, url, timestamp, last_published_date) VALUES (?, ?, ?, ?)', result)
        cursor.connection.commit()

    def get_last_published_date(self, url):
        response = requests.get(url)
        html_content = response.content.decode('utf-8')

        published_date = find_date(html_content)

        return published_date

@app.route('/api/search', methods=['POST'])
def search_handler():
    data = request.get_json()
    keyword = data.get('keyword', '')
    count = data.get('count', 10)
    
    google_search_handler = GoogleSearcher()
    google_search_handler._search_google(keyword, count)
    results = google_search_handler.results

    response = []
    for keyword, url, timestamp, last_published_date in results:
        response.append({
            'keyword': keyword,
            'url': url,
            'timestamp': timestamp,
            'last_published_date': last_published_date
        })
    return jsonify(response)

if __name__ == '__main__':
    app.run()
