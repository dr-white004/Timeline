
document.addEventListener('DOMContentLoaded', function() {
    prepare_posts();
});

function prepare_posts() {
    let posts = document.querySelectorAll("div.post-div");
    posts.forEach((post) => {
        const like_label = post.querySelector("span.like-count-label");
        like_label.addEventListener('click', () => like_post_click(post));
    });
}

function like_post_click(post) {
    console.log("CLICK");
    let post_id = post.querySelector("input.post-id").value;

    const csrftoken = getCookie('csrftoken');
    const like_label = post.querySelector("span.like-count-label");

    // Check if the post is currently liked or not
    const isLiked = like_label.classList.contains("liked-post");
    const like_action = isLiked ? 'unlike' : 'like'; // Toggle action based on current state

    const request = new Request(`/post/${post_id}/like`, {
        headers: { 'X-CSRFToken': csrftoken },
        method: 'POST',
        body: JSON.stringify({ action: like_action })
    });

    fetch(request)
        .then(response => response.json())
        .then(data => {
            handle_like_count(data["like_count"], data["like_status"]);
        })
        .catch(error => console.error('Error:', error)); // Handle any errors

    function handle_like_count(like_count, like_status) {
        like_label.innerText = like_count;
        if (like_status) {
            like_label.classList.add("liked-post");
        } else {
            like_label.classList.remove("liked-post");
        }
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();
}

function submitHandler(id) {
    const textareaValue = document.getElementById(`textarea_${id}`).value;
    const content = document.getElementById(`content_${id}`);
    const modal = document.getElementById(`modal_edit_post_${id}`);
    
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ content: textareaValue })
    })
    .then(response => response.json())
    .then(result => {
        content.innerHTML = result.data;
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none');

        // Remove modal backdrop
        const modalsBackdrops = document.getElementsByClassName('modal-backdrop');
        while (modalsBackdrops.length > 0) {
            document.body.removeChild(modalsBackdrops[0]);
        }
    })
    .catch(error => console.error('Error:', error)); // Handle any errors
}

