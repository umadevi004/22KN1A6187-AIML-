from flask import Flask, request, jsonify
import random
import string
app = Flask(__name__)
# In-memory database
url_store = {}
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400
    short_code = generate_short_code()
    url_store[short_code] = original_url
    return jsonify({
        'short_url': request.host_url + short_code,
        'original_url': original_url
    })
@app.route('/<short_code>')
def redirect_to_original(short_code):
    original_url = url_store.get(short_code)
    if original_url:
        return f'Redirect to: {original_url}', 302
    return jsonify({'error': 'Short URL not found'}), 404
@app.route('/')
def home():
    return "ShortURL API is running. Use POST /shorten to shorten a URL."
if __name__ == '__main__':
    app.run(debug=True)