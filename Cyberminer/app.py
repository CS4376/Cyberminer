from flask import Flask, render_template
from search_engine import GoogleSearcher

app = Flask(__name__)
searcher = GoogleSearcher()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    keyword = data['keyword']
    results = searcher.google_search(keyword)
    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
