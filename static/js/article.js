quill.format('align', 'right')
quill.format('direction', 'rtl')

quill.getModule('toolbar').addHandler('image', function() {
    document.getElementById('fileInput').click();
});

quill.getModule('toolbar').addHandler('video', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function() {
    let file = this.files[0];
    let formData = new FormData();
    formData.append('file', file)
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(url => {
        let range = quill.getSelection();
        if (file.type.startsWith('image/')) {
            quill.insertEmbed(range.index, 'image', url);
        } else if (file.type.startsWith('video/')) {
            quill.insertEmbed(range.index, 'video', url);
        }
    })
    .catch(error => {
        console.error('Error uploading file:', error);
    });
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

console.log('{{user.username}}')