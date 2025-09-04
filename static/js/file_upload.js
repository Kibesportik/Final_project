document.getElementById("file-input").addEventListener("change", function() {
    const emptyLabel = document.getElementById("file-name").dataset.emptyLabel;
    const fileName = this.files.length ? this.files[0].name : emptyLabel;
    document.getElementById("file-name").textContent = fileName;
});
