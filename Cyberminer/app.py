from flask import Flask, render_template, request, jsonify, redirect, url_for
from googlesearch import search
from autocorrect import Speller
import threading

app = Flask(__name__, static_url_path='/static')

class GoogleSearcher:
    def __init__(self):
        self.count = None
        self.keyword = None
        self.original_keyword = None
        self.results = []
        self.is_case_sensitive = False
        self.search_mode = 'OR'  # default.

    def display_searches(self, count):
        self.count = count

    def input_keyword(self, keyword, is_case_sensitive):
        spell = Speller(lang='en')
        self.keyword = spell(keyword) if not is_case_sensitive else keyword
        self.original_keyword = keyword
        self.is_case_sensitive = is_case_sensitive

    def input_search_mode(self, search_mode):
        self.search_mode = search_mode.upper() if search_mode.upper() in ['OR', 'AND', 'NOT'] else 'OR'

    def execute_search(self):
        try:
            self._search_google(self.keyword, self.count)
        except Exception as e:
            print(e)
            print("Google Search faced an Exception.")
        print("\nGoogle Search performed successfully.")

    def _search_google(self, keyword, count):
        # Search query depends on the selected mode.
        query = self.search_mode.join(keyword.split()) if self.search_mode in ['AND', 'OR'] else keyword.replace('NOT', '-')
        results = search(query, stop=count)
        self.results.append((keyword, list(results)))

    def get_results(self):
        return self.results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def execute_search():
    keyword = request.form.get('keyword')
    # Perform any necessary data validation or sanitization here

    # Instantiate the GoogleSearcher class
    google_searcher = GoogleSearcher()
    google_searcher.display_searches(10)  # Set the desired number of results
    google_searcher.input_keyword(keyword, False)  # Adjust the case sensitivity as needed
    google_searcher.input_search_mode('OR')  # Set the search mode: 'OR', 'AND', 'NOT'
    google_searcher.execute_search()

    # Redirect to the results page with the search query as a URL parameter
    return redirect(f'/results?keyword={keyword}')

@app.route('/results')
def results():
    keyword = request.args.get('keyword')

    # Instantiate the GoogleSearcher class
    google_searcher = GoogleSearcher()
    google_searcher.display_searches(10)  # Set the desired number of results
    google_searcher.input_keyword(keyword, False)  # Adjust the case sensitivity as needed
    google_searcher.input_search_mode('OR')  # Set the search mode: 'OR', 'AND', 'NOT'
    google_searcher.execute_search()
    search_results = google_searcher.get_results()

    return render_template('results.html', keyword=keyword, results=search_results)

if __name__ == '__main__':
    app.run()

