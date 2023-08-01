from flask import Flask, render_template, request, jsonify
from search_handler import GoogleSearcher

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    keyword = request.args.get('keyword', '')  # Get the 'keyword' parameter from the query string
    count = int(request.args.get('count', 10))  # Get the 'count' parameter from the query string and convert to an integer

    # Ensure count is not greater than 10
    count = min(count, 10)

    return render_template('results.html', keyword=keyword, count=count)


@app.route('/api/search', methods=['POST'])
def search_handler():
    try:
        data = request.get_json()
        keyword = data.get('keyword', '')
        count = int(data.get('count', 10))  # Convert count to an integer

        # Ensure count is not greater than 10
        count = min(count, 10)

        print(f"Received data: {data}")

        google_search_handler = GoogleSearcher()
        results = google_search_handler.search_google(keyword, count)

        print(f"Results: {results}")

        return jsonify(results)  # Return the search results as JSON data
    except AttributeError as e:
        print(f"AttributeError: {e}")
        return jsonify([]), 400  # Return an empty list with a 400 Bad Request status code if JSON data is not provided
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify([]), 500  # Return an empty list with a 500 Internal Server Error status code for any other errors
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)