#!/usr/bin/env python3
import os
import sys
import subprocess
import logging
import re
from github import Github
from github import GithubException

# Logging setup 
logging.basicConfig(filename="youtube_to_github.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def install_requirements():
    """Installs required Python packages if they are not already installed."""
    try:
        import pytube  
        if pytube.__version__ < '12.0.0':
            logging.warning("pytube version is old. Consider upgrading.")
    except ImportError:
        logging.info("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def main():
    # Default playlist ID (replace with your own if needed)
    default_playlist_id = "YOUR_DEFAULT_PLAYLIST_ID_HERE"  # Replace with a default if you want

    # Get playlist URL/ID from the user
    playlist_input = input(f"Enter YouTube playlist URL or ID (default: {default_playlist_id}): ")
    if not playlist_input:
        playlist_input = default_playlist_id

    # Construct the playlist URL if only the ID was provided
    if not playlist_input.startswith("https://"):
        playlist_url = f"https://www.youtube.com/playlist?list={playlist_input}"
    else:
        playlist_url = playlist_input

    try:
        # Import pytube here (inside try-except)
        from pytube import Playlist, exceptions
        playlist = Playlist(playlist_url)
        # Fix playlist video extraction
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

        videos = []
        for video in playlist.videos:
            try:
                videos.append((video.title, video.watch_url))
            except Exception as e:
                logging.error(f"Error processing video in playlist: {e}")

        videos.sort(key=lambda x: x[0])

        # Create .m3u file
        m3u_content = "#EXTM3U\n"
        for title, url in videos:
            m3u_content += f"#EXTINF:-1,{title}\n{url}\n"

        playlist_name = playlist.title 
        file_name = f"{playlist_name}.m3u"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(m3u_content)
        
        # Read file content into a variable 
        with open(file_name, "r", encoding="utf-8") as f:
            content = f.read()

        # GitHub interaction
        github_username = input("Enter GitHub username: ")
        github_repo = input("Enter GitHub repository name: ")
        github_token = input("Enter GitHub personal access token: ") or os.getenv("GITHUB_TOKEN")  # Prioritize input, but allow environment variable

        if not github_token:
            logging.error("No GitHub token provided.")
            return

        # Authenticate with GitHub
        g = Github(github_token)
        repo = g.get_user(github_username).get_repo(github_repo) 
        
        # Create or update file
        try:
            contents = repo.get_contents(file_name)
            repo.update_file(contents.path, "Update playlist", content, contents.sha)  # Pass content here
            logging.info(f"Playlist '{playlist_name}' updated on GitHub.")
        except GithubException as e:  # Catch all possible exceptions
            if e.status == 404:  # If file doesn't exist, create it
                repo.create_file(file_name, "Add playlist", content)  # Pass content here
                logging.info(f"Playlist '{playlist_name}' created on GitHub.")
            else:
                logging.error(f"An error occurred while updating/creating the file on GitHub: {e}")

    except exceptions.RegexMatchError:
        logging.error(f"Invalid playlist URL: {playlist_url}. Please check the format.")
    except KeyError:
        logging.error(f"Error extracting video information from the playlist: {playlist_url}")
    except ModuleNotFoundError:
        logging.error("The 'pytube' module is not installed. Please install it using 'pip install pytube'")
    except Exception as e:  # Catch all other exceptions
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    install_requirements()
    main()
