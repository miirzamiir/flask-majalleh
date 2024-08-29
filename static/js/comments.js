function showCommentForm() {
    const commentForm = document.getElementById('comment-form')
    commentForm.style.display = commentForm.style.display === 'none' ? 'block' : 'none';
}

function showReplyForm(id) {
    const replyForm = document.getElementById(`reply-form-${id}`);
    replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
}

function addComment() {
    const commentText = document.getElementById('comment-text').value;
    if (commentText.trim() === '') return;

    const comment = { text: commentText, title: title, username: username };


    fetch('/add-comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(comment)
    })
    .then(response => response.text())
    .then(url => {
        window.location.replace(url)
    });
}

function addReply(commentId) {
    const replyText = document.getElementById(`reply-text-${commentId}`).value;
    if (replyText.trim() === '') return;

    const reply = { text: replyText, title: title, username: username, parent_id: commentId };
    fetch('/add-comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reply)
    })
    .then(response => response.text())
    .then(url => {
        window.location.replace(url)
    });
}