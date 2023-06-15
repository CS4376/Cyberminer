from googlesearch import search
import sys
import webbrowser

class GoogleSearcher:
    def __init__(self):
        self.count = None
        self.keyword = None
        self.results = None

    def display_searches(self):
        print("\nEnter the total number of search results you want:")
        user_input = int(input())
        self.count = user_input

    def input_keyword(self):
        print("\nEnter the keyword for Google Search:")
        user_input = input()
        self.keyword = user_input

    def execute_search(self):
        try:
            results = search(self.keyword, num_results=self.count)
            self.results = list(results)
        except Exception as e:
            print(e)
            print("Google Search faced an Exception.")
        print("\nGoogle Search performed successfully.")

    def show_search_results(self):
        print(f"\nThe results for \"{self.keyword}\" keyword are:")
        count = 0
        page = 1
        total_results = len(self.results)
        num_pages = (total_results - 1) // 10 + 1
        visited_pages = []

        while count < total_results:
            visited_pages.append(page)
            print(f"\n--- Page {page} of {num_pages} ---")
            end_index = min(count + 10, total_results)

            for i in range(count, end_index):
                print(f"Search #{i + 1}: {self.results[i]}")

            print(f"\nShowing {count + 1}-{end_index} of {total_results} results.")

            if page > 1:
                print("\nPress 'b' to go back to the previous page.")
            if page <= num_pages:
                print("Press any key to view the next page or 'q' to quit:")
                choice = input()
                if choice.lower() == 'q':
                    break
                elif choice.lower() == 'b' and page > 1:
                    visited_pages.pop()
                    page = visited_pages.pop()
                    count = (page - 1) * 10
                    continue
                else:
                    count += 10
                    page += 1
            else:
                break

        print("\nEnd of search results.")

        self.open_hyperlink()
    
    def open_hyperlink(self):
        print("\nEnter the search number to open the corresponding URL in a web browser, or 'q' to quit:")
        choice = input()

        while choice.lower() != 'q':
            try:
                choice = int(choice)
                if 1 <= choice <= len(self.results):
                    url = self.results[choice - 1]
                    webbrowser.open_new_tab(url)
                    print(f"Opening URL: {url}")
                    print("\nEnter the search number to open the corresponding URL in a web browser, or 'q' to quit:")
                else:
                    print("Invalid search number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")
            choice = input()

        print("Exiting hyperlink enforcement.")
  

def main():
    google_search_handler = GoogleSearcher()
    print("\n--- Welcome to Cybermining ---\n")
    google_search_handler.display_searches()
    google_search_handler.input_keyword()
    google_search_handler.execute_search()
    google_search_handler.show_search_results()

if __name__ == '__main__':
    main()
