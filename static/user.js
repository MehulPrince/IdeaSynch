document.addEventListener("DOMContentLoaded", function () {
    const listCompanyBtn = document.getElementById("openListCompanyPopup"); // Match ID from HTML
    const popupForm = document.getElementById("listCompanyPopup"); // Match ID from HTML
    const closeBtn = document.getElementById("closePopup"); // Ensure this ID exists in HTML

    // Show popup when "List Company" button is clicked
    listCompanyBtn?.addEventListener("click", function () {
        popupForm.style.display = "flex";
    });

    // Close popup when "X" is clicked
    closeBtn?.addEventListener("click", function () {
        popupForm.style.display = "none";
    });

    // Close popup when clicking outside the form
    window.addEventListener("click", function (event) {
        if (event.target === popupForm) {
            popupForm.style.display = "none";
        }
    });
});
