// Check if user is logged in
const user = JSON.parse(localStorage.getItem("user"));
if (!user) {
    alert("Please login first");
    window.location.href = "login.html";
}

// Add Property Button Click
document.getElementById("addPropBtn").addEventListener("click", async () => {

    const title = document.getElementById("propTitle").value.trim();
    const price = document.getElementById("propPrice").value.trim();
    const location = document.getElementById("propLocation").value.trim();
    const description = document.getElementById("propDescription").value.trim();
    const status = document.getElementById("propStatus");

    // Quick validation
    if (!title || !price || !location) {
        status.style.color = "red";
        status.innerText = "Please fill all required fields.";
        return;
    }

    const data = {
        user_id: user.id,
        title,
        price,
        location,
        description
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/add_property", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        status.style.color = "green";
        status.innerText = result.message;

        // Clear fields on success
        document.getElementById("propTitle").value = "";
        document.getElementById("propPrice").value = "";
        document.getElementById("propLocation").value = "";
        document.getElementById("propDescription").value = "";

    } catch (error) {
        status.style.color = "red";
        status.innerText = "Server error!";
    }
});

// Logout
document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.clear();
    window.location.href = "login.html";
});
