document.getElementById('data-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    const preview = document.getElementById('image-preview')

    if (filename == '' && preview.src != window.location.href) {
        filename = preview.src
    }

	formData.append('profile_image', filename)
    fetch('/user/editpost', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(url => {
        window.location.replace(url)
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
