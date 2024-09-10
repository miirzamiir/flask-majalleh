quill.format('align', 'right')
quill.format('direction', 'rtl')

quill.getModule('toolbar').addHandler('image', function() {
    document.getElementById('image-input').click();
});

quill.getModule('toolbar').addHandler('video', function() {
    document.getElementById('video-input').click();
});

function upload(form, type) {
    fetch(`/upload-${type}`, {
        method: 'POST',
        body: form
    })
    .then(response => response.json())
    .then(data => {
        const messages = document.getElementById('messages')
        messages.innerHTML = ''
        if (data.error === undefined) {
            let range = quill.getSelection()
            quill.insertEmbed(range.index, type, data.url)
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
}

document.getElementById('image-input').addEventListener('change', function() {
    let file = this.files[0]
    let formData = new FormData()
    formData.append('file', file)
    upload(formData, 'image')
});

document.getElementById('video-input').addEventListener('change', function() {
    let file = this.files[0]
    let formData = new FormData()
    formData.append('file', file)
    upload(formData, 'video')
});

document.getElementById('data-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    const formData = new FormData(this); // Create a FormData object from the for
    // Add additional data to FormData
	if (quill.getLength() != 1) {
		formData.append('html-content', quill.root.innerHTML);
	}
	else {
		formData.append('html-content', '');
	}

    const preview = document.getElementById('image-preview')

    if (filename == '' && preview.src != window.location.href) {
        filename = preview.src
    }
	formData.append('image', filename)
    // Post data to the server
    fetch(path, {
        method: 'POST', // Specify the request method
        body: formData // Send the FormData object directly
    })
    .then(response => response.text())
    .then(url => {
        window.location.replace(url)
    })
    .catch((error) => {
        console.error('Error:', error); // Handle error
    });
});

window.addEventListener('load', function() {
    const btnGroups = document.querySelectorAll('.ql-formats .btn-group');
    btnGroups.forEach(btnGroup => {
            btnGroup.parentNode.removeChild(btnGroup);
        });
});
