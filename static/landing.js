// Add scrolled class to header on scroll
const header = document.getElementById("header");
window.addEventListener("scroll", () => {
  if (window.scrollY > 10) {
    header.classList.add("scrolled");
  } else {
    header.classList.remove("scrolled");
  }
});

// Ensure buttons navigate to correct Flask routes
document.querySelector(".btn-signin").addEventListener("click", function () {
  window.location.href = "/login";;
});

document.querySelector(".btn-register").addEventListener("click", function () {
  window.location.href = "/register";
});
