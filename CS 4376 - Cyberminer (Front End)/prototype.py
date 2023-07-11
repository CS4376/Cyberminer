from googlesearch import search
import threading
from autocorrect import Speller

class GoogleSearcher:
    def __init__(self):
        self.count = None
        self.keyword = None
        self.original_keyword = None
        self.results = []
        self.is_case_sensitive = False
        self.search_mode = 'OR'  # default.

    def display_searches(self):
        print("\nEnter the total number of search results you want:")
        user_input = int(input())
        self.count = user_input

    def input_keyword(self):
        print("\nEnter the keyword for Google Search:")
        user_input = input()
        spell = Speller(lang='en')
        self.keyword = spell(user_input) if not self.is_case_sensitive else user_input
        self.original_keyword = user_input

    def case_sensitive_search(self):
        print("\nDo you want to perform case sensitive search? (yes/no):")
        choice = input()
        self.is_case_sensitive = True if choice.lower() == 'yes' else False

    def input_search_mode(self):
        print("\nEnter the search mode: OR, AND, NOT")
        user_input = input()
        self.search_mode = user_input.upper() if user_input.upper() in ['OR', 'AND', 'NOT'] else 'OR'

    def execute_search(self):
        try:
            self.thread = threading.Thread(target=self._search_google, args=(self.keyword, self.count,))
            self.thread.start()
        except Exception as e:
            print(e)
            print("Google Search faced an Exception.")
        print("\nGoogle Search performed successfully.")

    def _search_google(self, keyword, count):
        #search query depends on selected mode.
        query = self.search_mode.join(keyword.split()) if self.search_mode in ['AND', 'OR'] else keyword.replace('NOT', '-')
        results = search(query, stop=count)
        self.results.append((keyword, list(results)))

    def show_search_results(self):
        self.thread.join()  # wait for thread to finish.
        print("\nThe results for the search are available now:")
        for keyword, results in self.results:
            print(f"\nThe results for \"{keyword}\" keyword are:")
            for i, result in enumerate(results):
                print(f"Search #{i + 1}: {result}")

def main():
    google_search_handlers = []
    while True:
        google_search_handler = GoogleSearcher()
        print("\n--- Welcome to Cybermining ---\n")
        google_search_handler.display_searches()
        google_search_handler.case_sensitive_search()
        google_search_handler.input_search_mode()
        google_search_handler.input_keyword()
        google_search_handler.execute_search()
        google_search_handlers.append(google_search_handler)

        print("\nDo you want to perform another search? (yes/no): ")
        choice = input()
        if choice.lower() != 'yes':
            break

    for handler in google_search_handlers:
        handler.show_search_results()

if __name__ == '__main__':
    main()
