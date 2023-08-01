from flask import Flask, render_template, request, jsonify
from search_handler import GoogleSearcher

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    data = request.args.get('data')  # Get the 'data' parameter from the query string
    return render_template('results.html', data=data)


@app.route('/api/search', methods=['POST'])
def search_handler():
    new_results = []
    try:
        data = request.get_json()
        keyword = data.get('keyword', '')
        count = int(data.get('count', 20))  # Convert count to an integer
        expiry_date = data.get('expiry_date')  # Get the expiry date
        all_results = data.get('all_results', False)

        # Ensure count is not greater than 10
        #count = min(count, 20)

        print(f"Received data: {data}")
        google_search_handler = GoogleSearcher()
        min_year = int(data.get('min_year', 2020))  # Convert min_year to an integer

        sortOrder = data.get('sortOrder', 'asc')
        search_mode = data.get('search_mode', 'OR')
        new_results = google_search_handler.search_google(keyword, count, expiry_date, min_year, sortOrder, search_mode=search_mode)
        print(f"Results: {google_search_handler.results}")

        if all_results:
            return jsonify(google_search_handler.results)  # Return all search results as JSON data
        else:
            return jsonify(new_results)  # Return only new results from the latest search
    except AttributeError as e:
        print(f"AttributeError: {e}")
        return jsonify([]), 400  # Return an empty list with a 400 Bad Request status code if JSON data is not provided
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify([]), 500  # Return an empty list with a 500 Internal Server Error status code for any other errors

if __name__ == '__main__':
    app.run(port=5000, debug=True)