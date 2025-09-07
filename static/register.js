const registerForm = document.getElementById("register-form");

registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(registerForm);
    const payload = {
        username: formData.get("username"),
        email: formData.get("email"),
        full_name: formData.get("full_name"),
        password: formData.get("password")
    };

    const response = await fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        alert("Registration successful! You can now login.");
        window.location.href = "/login";
    } else {
        const errorData = await response.json();
        alert(`Registration failed: ${errorData.detail}`);
    }
});
