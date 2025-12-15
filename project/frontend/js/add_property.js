
// Check if user is logged in
const user = JSON.parse(localStorage.getItem("user"));
if (!user) {
    alert("Please login first");
    window.location.href = "/project/frontend/pages/login.html";
}

// Add Property Button Click
document.getElementById("addPropBtn").addEventListener("click", async () => {

    const title = document.getElementById("propTitle").value.trim();
    const price = document.getElementById("propPrice").value.trim();
    const location = document.getElementById("propLocation").value.trim();
    const description = document.getElementById("propDescription").value.trim();
    const status = document.getElementById("propStatus");
    const imageFile = document.getElementById("propertyImage").files[0];

    // Validation
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
        // STEP 1️⃣ — ADD PROPERTY (existing API)
        const response = await fetch("http://127.0.0.1:5000/add_property", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!result.property_id) {
            status.style.color = "red";
            status.innerText = "Error adding property!";
            return;
        }

        status.style.color = "green";
        status.innerText = result.message;

        // STEP 2️⃣ — UPLOAD IMAGE if selected
        if (imageFile) {
            const formData = new FormData();
            formData.append("image", imageFile);

            const uploadResponse = await fetch(
                `http://127.0.0.1:5000/upload_image/${result.property_id}`,
                {
                    method: "POST",
                    body: formData
                }
            );

            const uploadResult = await uploadResponse.json();
            console.log("Image upload:", uploadResult);
        }

        // Clear fields after success
        document.getElementById("propTitle").value = "";
        document.getElementById("propPrice").value = "";
        document.getElementById("propLocation").value = "";
        document.getElementById("propDescription").value = "";
        document.getElementById("propertyImage").value = "";

    } catch (error) {
        console.error(error);
        status.style.color = "red";
        status.innerText = "Server error!";
    }
});

// Logout
document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.clear();
    window.location.href = "/project/frontend/pages/login.html";
});
