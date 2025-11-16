function deleteTodo(id) {
    fetch("/todo/delete", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(id)
    })
      .then(response => {
        console.log(response.json(), "response")
        if (response.ok) {
          alert("Item deleted successfully.");
          window.location.reload();
        }
        else {
          alert("Failed to delete selected item.")
        }
      })
      .catch(err => console.error(err));
    closeModal("DeleteTodo");
  }
  // Optional: Close modal on Escape key
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeModal();
  });