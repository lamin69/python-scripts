function updateFields() {
    var selector = document.getElementById("scriptSelector").value;
    document.getElementById("youtubeToGithubFields").style.display = selector === "youtube-to-github" ? "block" : "none";
    document.getElementById("channelScrapperFields").style.display = selector === "channel-scrapper" ? "block" : "none";
}

function runScript() {
    var scriptType = document.getElementById("scriptSelector").value;
    var data = {
        script_type: scriptType
    };

    if (scriptType === "youtube-to-github") {
        data.playlist_url = document.getElementById("playlistUrl").value;
        data.github_username = document.getElementById("githubUsername").value;
        data.github_repo = document.getElementById("githubRepo").value;
        data.github_token = document.getElementById("githubToken").value;
    } else if (scriptType === "channel-scrapper") {
        data.website_urls = document.getElementById("websiteUrls").value;
        data.github_username = document.getElementById("scrapperGithubUsername").value;
        data.github_repo = document.getElementById("scrapperGithubRepo").value;
        data.github_token = document.getElementById("scrapperGithubToken").value;
    }

    document.getElementById("progressBar").style.display = "block";
    document.getElementById("resultArea").style.display = "none";

    fetch('/run_script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        updateProgress(data.progress, data.message);
        if (data.content) {
            document.getElementById("resultContent").textContent = data.content;
            document.getElementById("resultArea").style.display = "block";
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function updateProgress(progress, message) {
    document.getElementById("progress").value = progress;
    document.getElementById("statusMessage").innerText = message;
}

function downloadResult() {
    var content = document.getElementById("resultContent").textContent;
    var blob = new Blob([content], { type: 'text/plain' });
    var url = window.URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'channels.m3u';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
}

function uploadToGithub() {
    var scriptType = document.getElementById("scriptSelector").value;
    var data = {
        script_type: scriptType + "_upload",
        content: document.getElementById("resultContent").textContent,
        github_username: document.getElementById(scriptType === "youtube-to-github" ? "githubUsername" : "scrapperGithubUsername").value,
        github_repo: document.getElementById(scriptType === "youtube-to-github" ? "githubRepo" : "scrapperGithubRepo").value,
        github_token: document.getElementById(scriptType === "youtube-to-github" ? "githubToken" : "scrapperGithubToken").value
    };

    fetch('/upload_to_github', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Upload Success:', data);
        alert(data.message);
    })
    .catch((error) => {
        console.error('Upload Error:', error);
        alert('Error uploading to GitHub');
    });
}

document.addEventListener('DOMContentLoaded', function() {
    updateFields();
});
