# python-scr YouTube Playlist to GitHub .m3u File Uploader ipts

YouTube Playlist to GitHub .m3u File Uploader

                                             Overview
                                             
This Python script automates the process of fetching a public YouTube playlist, converting it to an .m3u file, and uploading it to a GitHub repository. It's perfect for maintaining an up-to-date list of your favorite YouTube playlists in a format compatible with many media players.
Features
Fetches video titles and URLs from a public YouTube playlist
Creates an .m3u file with the playlist content
Uploads the .m3u file to a specified GitHub repository
Handles both creation and updating of files on GitHub
Provides detailed logging for troubleshooting
Requirements :
Python 3.6 or higher
pip (Python package installer)
GitHub account and personal access token
Required Python packages (installed via requirements.txt):
pytube
PyGithub
==========================================================
Installation
Clone the repository:
git clone https://github.com/lamin69/python-scripts.git

cd /lamin69/python-scripts

(Optional) Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  

# On Windows, use :  `venv\Scripts\activate`

Install the required packages:
pip install -r requirements.txt  
# the requirements to make the script works are in the file : requirements.txt

Make the script executable 
chmod +x youtube_to_github.py

Creating requirements.txt
If you need to create or update the requirements.txt file:
Ensure your virtual environment is activated (if you're using one).
Run the following command:
pip freeze > requirements.txt

this will create (or update) a requirements.txt file with all the currently installed packages in your environment.
Usage
Ensure you're in the project directory and your virtual environment is activated (if you're using one).
Run the script
./youtube_to_github.py   
or
python youtube_to_github.py

Setting Up GitHub Token
Go to your GitHub account settings
Navigate to "Developer settings" > "Personal access tokens" > "Tokens (classic)"
Click "Generate new token"
Give your token a descriptive name
Select the "repo" scope
Click "Generate token"
Copy the token and keep it secure (you won't be able to see it again)
Usage
Ensure you're in the project directory and your virtual environment is activated (if you're using one).
make the file excutable : chmod +x youtube_to_github.py
Run the script:   whatever you named it in this showcase the file name is : youtube_to_github.py

python youtube_to_github.py

When prompted, enter the YouTube playlist URL or ID. You can find the playlist ID in the URL of the playlist page (it's the value after ?list=).
The script will create an .m3u file with the playlist content.
You'll then be prompted for your GitHub details:
GitHub username
Repository name
Personal access token
The script will upload the .m3u file to your specified GitHub repository.
Troubleshooting
If you encounter any issues, check the youtube_to_github.log file for error messages.
Ensure your GitHub token has the necessary permissions (repo scope).
If you're having trouble with the pytube library, try updating it to the latest version:
text

Customization
You can set a default playlist ID by modifying the default_playlist_id variable in the script.
To avoid entering your GitHub token each time, you can set it as an environment variable named GITHUB_TOKEN.
Contributing
Contributions, issues, and feature requests are welcome! Feel free to check issues page.
License
[Include your chosen license here] This presentation provides a comprehensive overview of your script, including installation instructions, usage guidelines, and troubleshooting tips. You can further customize it to fit your specific needs or add any additional information you think would be helpful for users of your script. Remember to replace placeholders like yourusername, your-repo-name, and the link to the issues page with your actual GitHub details.
