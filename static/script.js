document.addEventListener("DOMContentLoaded", () => {
    // Set current year in footer
    document.getElementById("current-year").textContent = new Date().getFullYear()
  
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector(".mobile-menu-toggle")
    const mainNav = document.querySelector(".main-nav")
  
    if (mobileMenuToggle && mainNav) {
      mobileMenuToggle.addEventListener("click", function () {
        mainNav.classList.toggle("active")
        this.classList.toggle("active")
  
        // Add mobile menu styles dynamically when active
        if (mainNav.classList.contains("active")) {
          mainNav.style.display = "flex"
          mainNav.style.flexDirection = "column"
          mainNav.style.position = "absolute"
          mainNav.style.top = "var(--header-height)"
          mainNav.style.left = "0"
          mainNav.style.right = "0"
          mainNav.style.backgroundColor = "var(--color-background)"
          mainNav.style.padding = "1rem 2rem"
          mainNav.style.borderBottom = "1px solid var(--border-color)"
        } else {
          // Reset styles when inactive (for desktop view)
          if (window.innerWidth < 768) {
            mainNav.style.display = "none"
          } else {
            mainNav.style.display = "flex"
            mainNav.style.flexDirection = "row"
            mainNav.style.position = "static"
            mainNav.style.padding = "0"
            mainNav.style.border = "none"
          }
        }
      })
    }
  
    // Handle window resize for responsive menu
    window.addEventListener("resize", () => {
      if (window.innerWidth >= 768 && mainNav) {
        mainNav.style.display = "flex"
        mainNav.style.flexDirection = "row"
        mainNav.style.position = "static"
        mainNav.style.padding = "0"
        mainNav.style.border = "none"
  
        if (mobileMenuToggle) {
          mobileMenuToggle.classList.remove("active")
        }
        mainNav.classList.remove("active")
      } else if (window.innerWidth < 768 && mainNav && !mainNav.classList.contains("active")) {
        mainNav.style.display = "none"
      }
    })
  
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        e.preventDefault()
  
        const targetId = this.getAttribute("href")
        if (targetId === "#") return
  
        const targetElement = document.querySelector(targetId)
        if (targetElement) {
          const headerHeight = document.querySelector(".site-header").offsetHeight
          const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight
  
          window.scrollTo({
            top: targetPosition,
            behavior: "smooth",
          })
  
          // Close mobile menu if open
          if (mainNav && mainNav.classList.contains("active")) {
            mobileMenuToggle.click()
          }
        }
      })
    })
  
    // Add active class to nav links based on scroll position
    const sections = document.querySelectorAll("section[id]")
  
    function highlightNavLink() {
      const scrollPosition = window.scrollY
      const headerHeight = document.querySelector(".site-header").offsetHeight
  
      sections.forEach((section) => {
        const sectionTop = section.offsetTop - headerHeight - 100
        const sectionBottom = sectionTop + section.offsetHeight
        const sectionId = section.getAttribute("id")
  
        if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
          document.querySelectorAll(".nav-link").forEach((link) => {
            link.classList.remove("active")
            if (link.getAttribute("href") === `#${sectionId}`) {
              link.classList.add("active")
            }
          })
        }
      })
    }
  
    window.addEventListener("scroll", highlightNavLink)
  
    // Initialize active nav link on page load
    highlightNavLink()
  
    // Add active class styling
    const style = document.createElement("style")
    style.textContent = `
      .nav-link.active {
        color: var(--color-accent);
      }
      
      .mobile-menu-toggle.active span:nth-child(1) {
        transform: translateY(8px) rotate(45deg);
      }
      
      .mobile-menu-toggle.active span:nth-child(2) {
        opacity: 0;
      }
      
      .mobile-menu-toggle.active span:nth-child(3) {
        transform: translateY(-8px) rotate(-45deg);
      }
    `
    document.head.appendChild(style)
  })
  
