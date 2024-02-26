// Get the CSRF token from the cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(";").shift();
}

addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("#like_count").forEach((like_count) => {
        post_id = parseInt(like_count.dataset.post);

        fetch(`/like_count/${post_id}`).then((response) => {
            response.json().then((data) => {
                like_count.innerHTML = data.like_count;
            });
        });
    });

    document.querySelectorAll("#like_count").forEach((like_count) => {
        post_id = parseInt(like_count.dataset.post);

        fetch(`/like_count/${post_id}`).then((response) => {
            response.json().then((data) => {
                like_count.innerHTML = data.like_count;
            });
        });
    });

    // Like or Unlike button
    const like_button = document
        .querySelectorAll("#like_button")
        .forEach((button) => {
            button.onclick = () => {
                post_id = parseInt(button.dataset.post);
                user_id = button.dataset.user;

                fetch(`/likes/${user_id}`)
                    .then((response) => response.json())
                    .then((data) => {
                        liked_posts = data.liked_posts;

                        if (liked_posts.indexOf(post_id) >= 0) {
                            fetch(`/unlike/${post_id}`).then((response) => {
                                if (response.status != 200) {
                                    alert("Error unliking a post.");
                                }
                            });

                            button.innerHTML = `🤍`;

                            like_count = document.querySelector(
                                `#like_count[data-post="${post_id}"]`
                            );
                            old_like_count = parseInt(like_count.innerHTML);
                            like_count.innerHTML = old_like_count - 1;
                        } else {
                            fetch(`/like/${post_id}`).then((response) => {
                                if (response.status != 200) {
                                    alert("Error liking a post.");
                                }
                            });

                            button.innerHTML = `❤️`;

                            like_count = document.querySelector(
                                `#like_count[data-post="${post_id}"]`
                            );
                            old_like_count = parseInt(like_count.innerHTML);
                            like_count.innerHTML = old_like_count + 1;
                        }
                    });
            };
        });    
});
