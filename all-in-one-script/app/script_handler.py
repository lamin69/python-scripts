from youtube_to_github import run_youtube_to_github_script
from channel_scrapper import run_channel_scrapper_script
from github import Github
from github import GithubException

def run_youtube_to_github_handler(params):
    return run_youtube_to_github_script(
        params['playlist_url'],
        params['github_username'],
        params['github_repo'],
        params['github_token'],
        params['progress_callback']
    )

def run_channel_scrapper_handler(params):
    return run_channel_scrapper_script(
        params['website_urls'].split('\n'),
        params['progress_callback']
    )

def upload_to_github_handler(params):
    try:
        g = Github(params['github_token'])
        repo = g.get_user(params['github_username']).get_repo(params['github_repo'])
        file_name = 'channels.m3u' if params['script_type'] == 'channel-scrapper_upload' else 'playlist.m3u'
        
        try:
            contents = repo.get_contents(file_name)
            repo.update_file(contents.path, "Update M3U file", params['content'], contents.sha)
            return {"status": "success", "message": f"File '{file_name}' updated on GitHub."}
        except GithubException as e:
            if e.status == 404:
                repo.create_file(file_name, "Add M3U file", params['content'])
                return {"status": "success", "message": f"File '{file_name}' created on GitHub."}
            else:
                return {"status": "error", "message": f"An error occurred while updating/creating the file on GitHub: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
