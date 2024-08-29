document.getElementById('data-form').addEventListener('submit', function(event) {
    console.log('hello')
    event.preventDefault();
    const formData = new FormData(this);

	const preview = document.getElementById('image-preview')
	formData.append('profile_image', preview.src)
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
