import re
import logging
from github import Github
from github import GithubException
from pytube import Playlist, exceptions

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_youtube_to_github_script(playlist_url, github_username, github_repo, github_token, progress_callback):
    try:
        progress_callback(0, "Initializing...")
        playlist = Playlist(playlist_url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

        progress_callback(10, "Fetching playlist videos...")
        videos = []
        for i, video in enumerate(playlist.videos):
            try:
                videos.append((video.title, video.watch_url))
                progress = 10 + int((i + 1) / len(playlist.videos) * 40)
                progress_callback(progress, f"Processed {i + 1}/{len(playlist.videos)} videos")
            except Exception as e:
                logging.error(f"Error processing video in playlist: {e}")

        progress_callback(50, "Sorting videos...")
        videos.sort(key=lambda x: x[0])

        progress_callback(60, "Creating m3u content...")
        m3u_content = "#EXTM3U\n"
        for title, url in videos:
            m3u_content += f"#EXTINF:-1,{title}\n{url}\n"

        playlist_name = playlist.title 
        file_name = f"{playlist_name}.m3u"
        
        progress_callback(70, "Connecting to GitHub...")
        g = Github(github_token)
        repo = g.get_user(github_username).get_repo(github_repo) 
        
        try:
            progress_callback(80, "Checking if file exists on GitHub...")
            contents = repo.get_contents(file_name)
            progress_callback(90, "Updating existing file on GitHub...")
            repo.update_file(contents.path, f"Update playlist: {playlist_name}", m3u_content, contents.sha)
            return {"progress": 100, "message": f"Playlist '{playlist_name}' updated on GitHub."}
        except GithubException as e:
            if e.status == 404:
                progress_callback(90, "Creating new file on GitHub...")
                repo.create_file(file_name, f"Add playlist: {playlist_name}", m3u_content)
                return {"progress": 100, "message": f"Playlist '{playlist_name}' created on GitHub."}
            else:
                return {"progress": 100, "message": f"An error occurred while updating/creating the file on GitHub: {str(e)}"}

    except exceptions.RegexMatchError:
        return {"progress": 100, "message": f"Invalid playlist URL: {playlist_url}. Please check the format."}
    except KeyError:
        return {"progress": 100, "message": f"Error extracting video information from the playlist: {playlist_url}"}
    except Exception as e:
        return {"progress": 100, "message": f"An unexpected error occurred: {str(e)}"}
