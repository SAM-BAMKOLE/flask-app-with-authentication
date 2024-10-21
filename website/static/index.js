async function deleteNote(noteId) {
    await fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId }),
    });
    window.location.href = "/";
}

function editNote(noteId) {
    fetch("/edit-note", {
        method: "POST",
        body: JSON.stringify({ noteId }),
    }).then((res) => (window.location.href = "/"));
}
