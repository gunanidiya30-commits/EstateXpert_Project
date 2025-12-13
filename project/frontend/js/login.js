document.getElementById("loginBtn").addEventListener("click", async () => {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    const response = await fetch("http://localhost:5000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();

    if (result.status === "success") {
        alert("Login successful!");
        window.location.href = "index.html";  // redirect to dashboard/home
    } else {
        alert(result.message);
    }
});
