document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('playlistForm');
    const result = document.getElementById('result');
    const darkModeToggle = document.getElementById('darkModeToggle');
    const flashingTitle = document.getElementById('flashingTitle');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            result.innerHTML = data.message;
        })
        .catch(error => {
            result.innerHTML = 'An error occurred: ' + error;
        });
    });

    darkModeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
    });

    // Flashing title effect
    setInterval(() => {
        flashingTitle.style.opacity = flashingTitle.style.opacity === '1' ? '0.5' : '1';
    }, 500);
});
