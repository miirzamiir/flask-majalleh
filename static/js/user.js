document.getElementById('data-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);

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
