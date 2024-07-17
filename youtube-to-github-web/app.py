from flask import Flask, render_template, request, jsonify, send_from_directory
import script
import os

app = Flask(__name__, static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        playlist_url = request.form['playlist_url']
        github_username = request.form['github_username']
        github_repo = request.form['github_repo']
        github_token = request.form['github_token']
        
        result = script.run_script(playlist_url, github_username, github_repo, github_token)
        return jsonify(result)
    
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)