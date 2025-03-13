document.addEventListener("DOMContentLoaded", function () {
    const listCompanyBtn = document.getElementById("list-company-btn");
    const popupForm = document.getElementById("popup-form");
    const closeBtn = document.querySelector(".close");

    // Show popup when "List Company" button is clicked
    listCompanyBtn.addEventListener("click", function () {
        popupForm.style.display = "flex";
    });

    // Close popup when "X" is clicked
    closeBtn.addEventListener("click", function () {
        popupForm.style.display = "none";
    });

    // Close popup when clicking outside the form
    window.addEventListener("click", function (event) {
        if (event.target === popupForm) {
            popupForm.style.display = "none";
        }
    });
});
