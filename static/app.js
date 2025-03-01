

    
    // Handle form submission (login & register)
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", function (event) {
            const inputs = this.querySelectorAll("input[required]");
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add("error");
                } else {
                    input.classList.remove("error");
                }
            });

            if (!isValid) {
                event.preventDefault(); // Stop form submission if any field is empty
                alert("Please fill in all fields!");
            }
        });
    });

