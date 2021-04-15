function deleteBoard(boardId) {
  fetch("/delete-board", {
    method: "POST",
    body: JSON.stringify({ boardId: boardId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
