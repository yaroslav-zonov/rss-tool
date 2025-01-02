from flask import Flask, Response
from rss_processor import generate_rss
import os
import sys

app = Flask(__name__)

# Global variable to store the RSS content
rss_content = "https://comicsdb.ru/rss"

@app.route('/', methods=['GET'])
def serve_rss():
    global rss_content
    try:
        if not rss_content:
            rss_content = generate_rss()
        return Response(rss_content, mimetype='application/rss+xml')
    except Exception as e:
        print(f"Error serving RSS: {e}", file=sys.stderr)
        return "Error generating RSS feed", 500

@app.route('/api/update', methods=['GET'])
def update_rss():
    global rss_content
    try:
        rss_content = generate_rss()
        return "RSS updated successfully", 200
    except Exception as e:
        print(f"Error updating RSS: {e}", file=sys.stderr)
        return "Error updating RSS feed", 500

# This block is only for local testing
if __name__ == '__main__':
    rss_content = generate_rss()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

