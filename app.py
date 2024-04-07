from flask import Flask, render_template, request
import requests
import logging

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

logging.basicConfig(level=logging.DEBUG)

API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyBc9a2I57vkHjVYhJ42QkzMxZvwq0BY44k"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_query']
    if search_query:
        response = generate_story(search_query)
        logging.debug(f"API response: {response}")
        if response and 'candidates' in response:
            story_content = extract_story_content(response)
            if story_content:
                return render_template('result.html', story_content=story_content)
        error_msg = "Failed to generate story content. Please try again."
        return render_template('index.html', error=error_msg)
    else:
        error_msg = "Please enter a valid story prompt."
        return render_template('index.html', error=error_msg)

def generate_story(prompt):
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(API_ENDPOINT, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def extract_story_content(response):
    candidates = response['candidates']
    if candidates:
        content = candidates[0]['content']
        if content:
            parts = content['parts']
            if parts:
                return parts[0].get('text', '')
    return None

if __name__ == '__main__':
    app.run(debug=True)
