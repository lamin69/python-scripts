from flask import Flask, render_template, request, jsonify
from script_handler import run_youtube_to_github_handler, run_channel_scrapper_handler, upload_to_github_handler
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

current_progress = 0
status_message = ""
result_content = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    global current_progress, status_message, result_content
    data = request.json
    script_type = data['script_type']
    
    def progress_callback(progress, message):
        global current_progress, status_message
        current_progress = progress
        status_message = message
        logging.info(f"Progress: {progress}%, Message: {message}")
    
    data['progress_callback'] = progress_callback
    
    try:
        if script_type == 'youtube-to-github':
            result = run_youtube_to_github_handler(data)
        elif script_type == 'channel-scrapper':
            result = run_channel_scrapper_handler(data)
            result_content = result.get('content', '')
        else:
            return jsonify({'error': 'Invalid script type'}), 400
        
        result['content'] = result_content
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error running script: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/upload_to_github', methods=['POST'])
def upload_to_github():
    data = request.json
    try:
        result = upload_to_github_handler(data)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error uploading to GitHub: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/progress')
def progress():
    global current_progress, status_message
    return jsonify({'progress': current_progress, 'message': status_message})

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
