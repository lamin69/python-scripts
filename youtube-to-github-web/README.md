# YouTube Playlist to GitHub M3U Converter

This project provides a web application that automates the process of converting YouTube playlists into M3U files and uploading them directly to a specified GitHub repository. It offers a user-friendly web interface for easy interaction and management, packaged as a Docker container for simple deployment.

## Features

- **YouTube Playlist Conversion**: Automatically extracts video information from YouTube playlists.
- **M3U File Generation**: Creates standardized M3U playlist files from YouTube playlists.
- **GitHub Integration**: Seamlessly uploads generated M3U files to a specified GitHub repository.
- **Web Interface**: Offers a modern, responsive web UI for easy interaction.
- **Dark Mode**: Includes a toggle for dark mode, enhancing user experience in different lighting conditions.
- **Docker Support**: Easily deployable using Docker and Docker Compose.

## Tech Stack

- **Backend**: Python with Flask framework
- **Frontend**: HTML5, CSS3, JavaScript
- **Container**: Docker
- **External APIs**: YouTube Data API, GitHub API

## Project Structure
youtube-to-github/

├── app.py

├── script.py

├── static/

│ ├── css/

│ │ └── styles.css

│ └── js/

│ └── main.js

├── templates/

│ └── index.html

├── requirements.txt

├── Dockerfile

└── docker-compose.yml

## Key Components

- `app.py`: Flask application serving as the web server and API endpoint.
- `script.py`: Core functionality for processing YouTube playlists and GitHub uploads.
- `static/css/styles.css`: Styling for the web interface, including dark mode.
- `static/js/main.js`: Client-side JavaScript for enhanced user interaction.
- `templates/index.html`: HTML template for the web interface.
- `Dockerfile`: Instructions for building the Docker image.
- `docker-compose.yml`: Defines and runs the multi-container Docker application.

## Setup and Deployment

1. Clone the repository:
2. git clone https://github.com/lamin69/youtube-to-github-web.git
 
3. cd youtube-to-github
  
4. Build and run using Docker Compose:

5. docker-compose up -d
Check: https://hub.docker.com/r/lamin69/youtube-to-github

3. Access the web interface at http://localhost:5000 (or your server's IP address).

## Configuration

Create a `.env` file in the project root to configure environment variables:

FLASK_ENV=production

FLASK_APP=app.py

FLASK_DEBUG=0

GITHUB_TOKEN=your_github_token_here

YOUTUBE_API_KEY=your_youtube_api_key_here

LOG_PATH=./logs

CONFIG_PATH=./config

RESTART_POLICY=unless-stopped

CPU_LIMIT=0.5

MEMORY_LIMIT=512M

## Usage

1. Open the web interface in a browser.
2. Enter the YouTube playlist URL, GitHub username, repository name, and personal access token.
3. Click "Submit" to start the conversion and upload process.
4. The application will process the playlist, create an M3U file, and upload it to the specified GitHub repository.

## Security Note

This application requires a GitHub Personal Access Token. Ensure you're using this in a secure environment and never share your token publicly.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the issues page if you want to contribute.

## License

MIT

## Author

69lamin

## Acknowledgments

- YouTube Data API
- PyGithub library
- Flask framework
- Docker and Docker Compose

This project aims to simplify the process of archiving YouTube playlists as M3U files on GitHub, providing an easy-to-use interface and leveraging Docker for simple deployment and scalability.
