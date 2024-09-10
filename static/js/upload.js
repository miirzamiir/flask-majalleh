let filename = ''

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
    filename = ''
}

document.getElementById('profile-pic').addEventListener('change', function() {
	let file = this.files[0]
    let formData = new FormData()
    formData.append('file', file)
    fetch('/upload-image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const messages = document.getElementById('messages')
        messages.innerHTML = ''
        if (data.error === undefined) {
            let url = data.url
		    const preview = document.getElementById('image-preview');
		    const deleteButton = document.getElementById('delete-button');
		    deleteButton.style.display = 'block'
		    preview.src = url;
            filename = url
		    preview.style.display = 'block'
        }
        else {
            const divMsg = document.createElement('div')
            divMsg.className = 'alert alert-danger'
            divMsg.innerHTML = data.message
            messages.appendChild(divMsg)
        }  
    })
    .catch(error => {
        console.log(error)
    });
})

