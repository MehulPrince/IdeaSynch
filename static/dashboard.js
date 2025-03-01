document.addEventListener("DOMContentLoaded", function () {
    // Example: Search functionality
    const searchInput = document.getElementById("search");
    searchInput.addEventListener("keyup", function () {
        let filter = searchInput.value.toLowerCase();
        let cards = document.querySelectorAll(".startup-card");

        cards.forEach(card => {
            let title = card.querySelector("h3").innerText.toLowerCase();
            if (title.includes(filter)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
});
