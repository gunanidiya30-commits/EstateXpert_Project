document.getElementById("loginBtn").addEventListener("click", async function () {
    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value.trim();

    const resultBox = document.getElementById("loginStatus");
    resultBox.innerText = "Checking...";

    try {
        const response = await fetch("http://127.0.0.1:5000/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            resultBox.style.color = "green";
            resultBox.innerText = "Login successful! Redirecting...";

            setTimeout(() => {
                window.location.href = "../index.html";


            }, 1500);
        } else {
            resultBox.style.color = "red";
            resultBox.innerText = data.error || "Invalid email or password!";
        }
    } catch (err) {
        resultBox.style.color = "red";
        resultBox.innerText = "Server offline.";
    }
});
