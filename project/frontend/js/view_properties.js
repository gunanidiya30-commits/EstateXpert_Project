const user = JSON.parse(localStorage.getItem("user"));
if (!user) {
    alert("Please login first");
    window.location.href = "login.html";
}

async function loadProperties() {
    const container = document.getElementById("propertyContainer");

    const response = await fetch(`http://127.0.0.1:5000/get_properties/${user.id}`);
    const data = await response.json();

    container.innerHTML = "";

    if (!Array.isArray(data) || data.length === 0) {
        container.innerHTML = "<p>No properties added yet.</p>";
        return;
    }

    data.forEach(p => {
        const card = `
            <div class="property-card">
                <h3>${p.title}</h3>
                <p><b>Price:</b> ₹${p.price}</p>
                <p><b>Location:</b> ${p.location}</p>
                <p>${p.description}</p>
                <span class="date">Added on: ${p.created_at}</span>

                <button class="delete-btn" onclick="deleteProperty(${p.id})">Delete</button>
            </div>
        `;

        container.innerHTML += card;   // 🔥 THIS WAS MISSING
    });
}

async function deleteProperty(id) {
    const confirmDelete = confirm("Are you sure you want to delete this property?");
    if (!confirmDelete) return;

    const response = await fetch(`http://127.0.0.1:5000/delete_property/${id}`, {
        method: "DELETE"
    });

    const result = await response.json();

    if (result.message) {
        alert("Property deleted successfully!");
        loadProperties();  // refresh the list
    } else {
        alert("Error deleting property.");
    }
}


// Load properties on page load
loadProperties();

// Logout
document.getElementById("logoutBtn").onclick = () => {
    localStorage.clear();
    window.location.href = "login.html";
};
