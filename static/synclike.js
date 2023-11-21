// JavaScript code to handle asynchronous requests when the like button is clicked 
document.addEventListener('DOMContentLoaded', function () {

            document.addEventListener('DOMContentLoaded', function () {
                document.querySelectorAll('.like-form').forEach(function (form) {
                    form.addEventListener('submit', function (event) {
                        event.preventDefault();
                        const postId = event.target.getAttribute('action').split('/').pop();
                        const likeCountSpan = document.getElementById('like-count-' + postId);
                        const likeBtn = document.getElementById('like-btn-' + postId);
        
                        fetch(event.target.getAttribute('action'), {
                            method: 'POST',
                            credentials: 'include',
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                likeCountSpan.innerText = data.likes;
                                if (data.action === 'like') {
                                    likeBtn.innerText = '👎';
                                } else {
                                    likeBtn.innerText = '👍';
                                }
                                likeBtn.disabled = true;
                            } else {
                                alert(data.message);
                            }
                        })
                        .catch(error => console.error('Error:', error));
                    });
                });
            });
        });