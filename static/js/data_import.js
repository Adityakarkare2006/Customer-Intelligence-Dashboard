document.addEventListener("DOMContentLoaded", () => {

    const fileInput = document.getElementById("file");
    const fileName = document.getElementById("fileName");
    const uploadArea = document.querySelector(".upload-area");
    const importForm = document.getElementById("importForm");
    const uploadButton = document.querySelector(".upload-btn");

    if (!fileInput || !fileName || !uploadArea || !importForm) {
        return;
    }

    // File selection
    fileInput.addEventListener("change", () => {

        if (!fileInput.files.length) {
            fileName.textContent = "Choose a file or drag & drop";
            return;
        }

        const file = fileInput.files[0];
        const extension = file.name.split(".").pop().toLowerCase();

        if (!["csv", "xlsx"].includes(extension)) {
            fileInput.value = "";
            fileName.textContent = "Choose a file or drag & drop";

            alert("Please select a CSV or Excel (.xlsx) file.");
            return;
        }

        fileName.textContent = file.name;
    });


    // Drag over
    uploadArea.addEventListener("dragover", (event) => {
        event.preventDefault();
        uploadArea.classList.add("drag-active");
    });


    // Drag leave
    uploadArea.addEventListener("dragleave", () => {
        uploadArea.classList.remove("drag-active");
    });


    // Drop file
    uploadArea.addEventListener("drop", (event) => {

        event.preventDefault();
        uploadArea.classList.remove("drag-active");

        const files = event.dataTransfer.files;

        if (!files.length) {
            return;
        }

        const file = files[0];
        const extension = file.name.split(".").pop().toLowerCase();

        if (!["csv", "xlsx"].includes(extension)) {
            alert("Please upload a CSV or Excel (.xlsx) file.");
            return;
        }

        fileInput.files = files;
        fileName.textContent = file.name;
    });


    // Form submit
    importForm.addEventListener("submit", () => {

        if (!fileInput.files.length) {
            return;
        }

        uploadButton.disabled = true;

        uploadButton.innerHTML = `
            <i class="ri-loader-4-line"></i>
            Uploading...
        `;
    });

});