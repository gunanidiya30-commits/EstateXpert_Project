document.getElementById("signupForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    const resultBox = document.getElementById("result");
    resultBox.innerText = "Processing...";

    try {
        const response = await fetch("http://127.0.0.1:5000/api/auth/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            resultBox.style.color = "green";
            resultBox.innerText = "Signup successful! Redirecting...";
            setTimeout(() => {
                window.location.href = "login.html";
            }, 1500);
        } else {
            resultBox.style.color = "red";
            resultBox.innerText = data.error || "Signup failed.";
        }
    } catch (err) {
        resultBox.innerText = "Server not reachable.";
        resultBox.style.color = "red";
    }
});
