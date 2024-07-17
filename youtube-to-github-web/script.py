import os
import re
import logging
from github import Github
from github import GithubException
from pytube import Playlist, exceptions

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_script(playlist_url, github_username, github_repo, github_token):
    try:
        playlist = Playlist(playlist_url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

        videos = []
        for video in playlist.videos:
            try:
                videos.append((video.title, video.watch_url))
            except Exception as e:
                logging.error(f"Error processing video in playlist: {e}")

        videos.sort(key=lambda x: x[0])

        m3u_content = "#EXTM3U\n"
        for title, url in videos:
            m3u_content += f"#EXTINF:-1,{title}\n{url}\n"

        playlist_name = playlist.title 
        file_name = f"{playlist_name}.m3u"
        
        g = Github(github_token)
        repo = g.get_user(github_username).get_repo(github_repo) 
        
        try:
            contents = repo.get_contents(file_name)
            repo.update_file(contents.path, "Update playlist", m3u_content, contents.sha)
            return {"status": "success", "message": f"Playlist '{playlist_name}' updated on GitHub."}
        except GithubException as e:
            if e.status == 404:
                repo.create_file(file_name, "Add playlist", m3u_content)
                return {"status": "success", "message": f"Playlist '{playlist_name}' created on GitHub."}
            else:
                return {"status": "error", "message": f"An error occurred while updating/creating the file on GitHub: {str(e)}"}

    except exceptions.RegexMatchError:
        return {"status": "error", "message": f"Invalid playlist URL: {playlist_url}. Please check the format."}
    except KeyError:
        return {"status": "error", "message": f"Error extracting video information from the playlist: {playlist_url}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}