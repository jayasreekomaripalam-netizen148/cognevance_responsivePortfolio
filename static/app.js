// ================= MOBILE MENU =================

const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

if (menuToggle && navLinks) {

    menuToggle.addEventListener("click", () => {
        navLinks.classList.toggle("active");
    });

    document.querySelectorAll(".nav-links a").forEach((link) => {

        link.addEventListener("click", () => {
            navLinks.classList.remove("active");
        });

    });

}


// ================= THEME TOGGLE =================

const themeToggle = document.getElementById("themeToggle");

const savedTheme = localStorage.getItem("portfolio-theme");

if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
}

if (themeToggle) {

    themeToggle.addEventListener("click", () => {

        document.body.classList.toggle("dark-mode");

        const currentTheme =
            document.body.classList.contains("dark-mode")
                ? "dark"
                : "light";

        localStorage.setItem(
            "portfolio-theme",
            currentTheme
        );

    });

}


// ================= CONTACT FORM =================

const contactForm = document.getElementById("contactForm");
const responseBox = document.getElementById("response");

if (contactForm) {

    contactForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const name =
            document.getElementById("name").value.trim();

        const email =
            document.getElementById("email").value.trim();

        const message =
            document.getElementById("message").value.trim();

        const submitButton =
            contactForm.querySelector("button[type='submit']");


        // Validation

        if (name.length < 2) {

            responseBox.textContent =
                "Please enter a valid name.";

            return;
        }


        const emailPattern =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {

            responseBox.textContent =
                "Please enter a valid email address.";

            return;
        }


        if (message.length < 10) {

            responseBox.textContent =
                "Message must contain at least 10 characters.";

            return;
        }


        // Sending state

        submitButton.disabled = true;

        submitButton.textContent = "Sending...";

        responseBox.textContent = "";


        try {

            const response = await fetch(
                "/api/contact",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        email: email,
                        message: message
                    })
                }
            );


            const data = await response.json();


            if (data.success) {

                responseBox.textContent =
                    "✓ " + data.message;

                contactForm.reset();

            } else {

                responseBox.textContent =
                    data.message ||
                    "Something went wrong.";

            }

        } catch (error) {

            console.error(error);

            responseBox.textContent =
                "Unable to connect to the server.";

        }


        submitButton.disabled = false;

        submitButton.textContent = "Send Message";

    });

}


// ================= SCROLL REVEAL =================

// IMPORTANT:
// Make every reveal element visible first.
// This prevents the whole website from becoming
// invisible if JavaScript fails.

const revealElements =
    document.querySelectorAll(".reveal");

revealElements.forEach((element) => {

    element.classList.add("visible");

});


// Optional animation when IntersectionObserver
// is supported.

if ("IntersectionObserver" in window) {

    const observer =
        new IntersectionObserver(
            (entries) => {

                entries.forEach((entry) => {

                    if (entry.isIntersecting) {

                        entry.target.classList.add("visible");

                    }

                });

            },
            {
                threshold: 0.1
            }
        );


    revealElements.forEach((element) => {

        observer.observe(element);

    });

}


// ================= ACTIVE NAVIGATION =================

const sections =
    document.querySelectorAll("section[id]");

const navigationLinks =
    document.querySelectorAll(".nav-links a");

if ("IntersectionObserver" in window) {

    const sectionObserver =
        new IntersectionObserver(
            (entries) => {

                entries.forEach((entry) => {

                    if (entry.isIntersecting) {

                        navigationLinks.forEach((link) => {

                            link.classList.remove("active");

                            if (
                                link.getAttribute("href") ===
                                "#" + entry.target.id
                            ) {

                                link.classList.add("active");

                            }

                        });

                    }

                });

            },
            {
                threshold: 0.35
            }
        );


    sections.forEach((section) => {

        sectionObserver.observe(section);

    });

}

