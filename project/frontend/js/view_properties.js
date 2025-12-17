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
        const imgSrc = p.image
            ? `http://127.0.0.1:5000/uploads/${p.image}`
            : "default.jpg";

        const card = `
            <div class="property-card">
                <img src="${imgSrc}" class="property-image" alt="Property Image">
                <h3>${p.title}</h3>
                <p><b>Price:</b> ₹${p.price}</p>
                <p><b>Location:</b> ${p.location}</p>
                <p>${p.description}</p>
                <span class="date">Added on: ${p.created_at}</span>

                <button class="delete-btn" onclick="deleteProperty(${p.id})">Delete</button>
                <button class="edit-btn" onclick="editProperty(${p.id})">Edit</button>
            </div>
        `;

        container.innerHTML += card;
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
        loadProperties();
    } else {
        alert("Error deleting property.");
    }
}

function editProperty(id) {
    localStorage.setItem("edit_property_id", id);
    window.location.href = "edit_property.html";
}

// Load properties on page load
loadProperties();

// 🔍 Real‑time Search Filtering
document.getElementById('searchInput').addEventListener('keyup', function () {
    let query = this.value.toLowerCase().trim();
    let cards = document.getElementsByClassName('property-card');

    let found = false; // Track if any card matches

    for (let card of cards) {
        let text = card.innerText.toLowerCase();
        let match = text.includes(query);

        card.style.display = match ? "block" : "none";

        if (match) found = true;
    }

    // Show / Hide "No Results" message
    document.getElementById("noResults").style.display = found ? "none" : "block";
});


// Logout
document.getElementById("logoutBtn").onclick = () => {
    localStorage.clear();
    window.location.href = "login.html";
};
