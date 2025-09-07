const loginForm = document.getElementById("login-form");

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(loginForm);
    const response = await fetch("/token", {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        window.location.href = "/";
    } else {
        alert("Login failed!");
    }
});
