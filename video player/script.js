document.getElementById('videoUpload').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const videoPlayer = document.getElementById('videoPlayer');
        const videoSource = document.getElementById('videoSource');
        const fileURL = URL.createObjectURL(file);
        videoSource.src = fileURL;
        videoPlayer.load();
        videoPlayer.style.display = 'block';
    }
});

document.getElementById('generateSubtitles').addEventListener('click', async function () {
    const fileInput = document.getElementById('videoUpload');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please upload a video file first.');
        return;
    }

    const status = document.getElementById('status');
    status.textContent = 'Generating subtitles...';

    // Send the video file to the backend for subtitle generation
    const formData = new FormData();
    formData.append('video', file);

    try {
        const response = await fetch('/generate-subtitles', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            status.textContent = 'Subtitles generated successfully!';
            const videoPlayer = document.getElementById('videoPlayer');
            videoPlayer.innerHTML += `<track label="English" kind="subtitles" srclang="en" src="${result.subtitleUrl}" default>`;
        } else {
            status.textContent = 'Error generating subtitles.';
        }
    } catch (error) {
        status.textContent = 'Error generating subtitles.';
        console.error(error);
    }
});