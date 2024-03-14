from flask import Flask, jsonify, request
from flask_cors import CORS
import config

from query import Query
import summarize

query = Query(f"{config.indexes_path}A.json", "ids.json")   
app = Flask(__name__)
CORS(app)

@app.route("/search")
def search():
    args = request.args.get('query')
    parsed = query.parse_query(args)
    pages = query.get_top_ten()
    return jsonify(pages)

@app.route("/summary")
def summary():
    args = request.args.get('url')
    return jsonify(summarize.summarize(args))

if __name__ == '__main__':
    app.run(debug=True)