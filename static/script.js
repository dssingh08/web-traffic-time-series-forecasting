const predictForm = document.getElementById("predict-form");
const resultDiv = document.getElementById("result");

const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "/login";
}

predictForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(predictForm);
    const payload = {
        model_name: formData.get("model_name"),
        days: parseInt(formData.get("days"))
    };

    const response = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        const data = await response.json();
        resultDiv.innerHTML = `<img src="${data.plot_path}?t=${new Date().getTime()}" />`;
    } else {
        alert("Prediction failed!");
    }
});
