function deleteImage() {
    const preview = document.getElementById('image-preview');
    if (!preview.src) {
        return;
    }
    const deleteButton = document.getElementById('delete-button');
    preview.src = '';
    preview.style.display = 'none';
    deleteButton.style.display = 'none';
    document.getElementById('profile-pic').value = '';
    const formData = new FormData();
    formData.append('filename', preview.src);
}

document.getElementById('profile-pic').addEventListener('change', function() {
	let file = this.files[0];
    let formData = new FormData();
    formData.append('file', file)
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(url => {
		const preview = document.getElementById('image-preview');
		const deleteButton = document.getElementById('delete-button');
		deleteButton.style.display = 'block'
		preview.src = url;
		preview.style.display = 'block'
    })
    .catch(error => {
        console.error('Error uploading file:', error);
    });
})

