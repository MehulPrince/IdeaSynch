document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector(".sidebar");
    const toggleBtn = document.getElementById("toggle-sidebar");
    const userTab = document.getElementById("user-tab");
    const popup = document.getElementById("company-popup");
    const closeBtn = document.querySelector(".close-btn");
    const companyForm = document.getElementById("company-form");

    // Sidebar Toggle
    toggleBtn.addEventListener("click", function () {
        sidebar.classList.toggle("show");
        if (sidebar.classList.contains("show")) {
            toggleBtn.innerHTML = "←"; // Change icon
        } else {
            toggleBtn.innerHTML = "➤";
        }
    });

    // Open User Page
    userTab.addEventListener("click", function (event) {
        event.preventDefault();
        window.location.href = "/user"; // Redirect to user page
    });

    // Open Popup
    document.querySelector(".list-company").addEventListener("click", function () {
        popup.style.display = "block";
    });

    // Close Popup
    closeBtn.addEventListener("click", function () {
        popup.style.display = "none";
    });

    // Handle Company Form Submission
    companyForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const data = {
            name: document.getElementById("company-name").value,
            description: document.getElementById("company-description").value,
            sector: document.getElementById("company-sector").value,
            funding_required: document.getElementById("funding-required").value,
            founder_details: document.getElementById("founder-details").value,
            education: document.getElementById("education").value,
            existing_funding: document.getElementById("existing-funding").value
        };

        fetch("/list_company", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            alert(result.message);
            popup.style.display = "none";
            location.reload(); // Refresh to show the new company
        })
        .catch(error => console.error("Error:", error));
    });
});
