function deletePost(PostId) {
  fetch("/delete_post", {
    method: "POST",
    body: JSON.stringify({ PostId: PostId }),
  }).then((_res) => {
    window.location.reload();
  });
}
function deletePostComment(CommentId) {
  fetch("/delete_post_comment", {
    method: "POST",
    body: JSON.stringify({ CommentId: CommentId }),
  }).then((_res) => {
    window.location.reload();
  });
}
function deleteMessage(MessageId) {
  fetch("/delete_message", {
    method: "POST",
    body: JSON.stringify({ MessageId: MessageId }),
  }).then((_res) => {
    window.location.reload();
  });
}

function addInterest(InterestId) {
  fetch("/add_interest", {
    method: "POST",
    body: JSON.stringify({ InterestId: InterestId }),
  }).then((_res) => {
    //window.location.href = "/choose_interests";
    window.location.reload();
  });
}

function like(postId) {
  const likeCount = document.getElementById(`likes-count-${postId}`);
  const likeExt = document.getElementById(`likes-ext-${postId}`);
  const likeButton = document.getElementById(`like-button-${postId}`);

  fetch(`/like-post/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      likeCount.innerHTML = data["likes"];
      if (data["liked"] === true) {
        likeButton.className = "fas fa-thumbs-up";
      } else {
        likeButton.className = "far fa-thumbs-up";
      }
      if (likeCount.innerHTML == 1) {
        likeExt.innerHTML = " like";
      } else {
        likeExt.innerHTML = " likes";
      }
    })
    .catch((e) => alert("Could not like post."));
}

function join(groupId) {
  const joinButton = document.getElementById(`join-${groupId}`);
  const membersCount = document.getElementById(`members-count-${groupId}`);

  fetch(`/join-group/${groupId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      membersCount.innerHTML = data["members"];
      if (data["joined"] === true) {
        joinButton.innerHTML = "Leave Group";
      } else {
        joinButton.innerHTML = "Join Group";
      }
    })
    .catch((e) => alert(groupId));
}
