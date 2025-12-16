// -----------------------------
// CHECK LOGIN
// -----------------------------


if (!user) {
    alert("Please login first");
    window.location.href = "login.html";
}

// -----------------------------
// ADD PROPERTY
// -----------------------------
document.getElementById("addPropBtn").addEventListener("click", async (e) => {
    e.preventDefault(); // ✅ STOP FORM SUBMIT

    const title = document.getElementById("propTitle").value.trim();
    const price = document.getElementById("propPrice").value.trim();
    const location = document.getElementById("propLocation").value.trim();
    const description = document.getElementById("propDescription").value.trim();
    const imageFile = document.getElementById("propertyImage").files[0];
    const status = document.getElementById("propStatus");

    if (!title || !price || !location) {
        status.style.color = "red";
        status.innerText = "Please fill all required fields.";
        return;
    }

    try {
        // STEP 1 — CREATE PROPERTY
        const response = await fetch("http://127.0.0.1:5000/api/add_property", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: user.id,
                title,
                price,
                location,
                description
            })
        });

        const result = await response.json();

        if (!result.property_id) {
            status.style.color = "red";
            status.innerText = "Failed to add property.";
            return;
        }

        // STEP 2 — IMAGE UPLOAD
        if (imageFile) {
            const formData = new FormData();
            formData.append("image", imageFile);

            const uploadResponse = await fetch(
                `http://127.0.0.1:5000/api/upload_image/${result.property_id}`,
                {
                    method: "POST",
                    body: formData
                }
            );

            const uploadResult = await uploadResponse.json();

            if (!uploadResult.message) {
                status.style.color = "red";
                status.innerText = "Property added, but image upload failed.";
                return;
            }
        }

        // SUCCESS
        status.style.color = "green";
        status.innerText = "Property added successfully!";

        // CLEAR FORM
        document.getElementById("addPropertyForm").reset();

    } catch (err) {
        console.error(err);
        status.style.color = "red";
        status.innerText = "Server error!";
    }
});

// -----------------------------
// LOGOUT
// -----------------------------
document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.clear();
    window.location.href = "login.html";
});
