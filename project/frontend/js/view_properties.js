const user = JSON.parse(localStorage.getItem("user"));
if (!user) {
    alert("Please login first");
    window.location.href = "login.html";
}

let properties = []; // GLOBAL ARRAY to store all properties

async function loadProperties() {
    const container = document.getElementById("propertyContainer");

    const response = await fetch(`http://127.0.0.1:5000/get_properties/${user.id}`);
    const data = await response.json();
    properties = data; // store properties globally

    renderProperties(properties);
}

function renderProperties(list) {
    const container = document.getElementById("propertyContainer");
    container.innerHTML = "";

    if (!Array.isArray(list) || list.length === 0) {
        container.innerHTML = "<p>No properties added yet.</p>";
        return;
    }

    list.forEach(p => {
        const imgSrc = p.image
            ? `http://127.0.0.1:5000/uploads/${p.image}`
            : "default.jpg";

        container.innerHTML += `
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

    let found = false;

    for (let card of cards) {
        let text = card.innerText.toLowerCase();
        let match = text.includes(query);

        card.style.display = match ? "block" : "none";

        if (match) found = true;
    }

    document.getElementById("noResults").style.display = found ? "none" : "block";
});

// Sorting
document.getElementById("sortSelect").addEventListener("change", function () {
    let option = this.value;

    if (option === "priceAsc") {
        properties.sort((a, b) => a.price - b.price);
    }
    else if (option === "priceDesc") {
        properties.sort((a, b) => b.price - a.price);
    }
    else if (option === "nameAsc") {
        properties.sort((a, b) => a.title.localeCompare(b.title));
    }
    else if (option === "nameDesc") {
        properties.sort((a, b) => b.title.localeCompare(a.title));
    }
    else if (option === "newest") {
        properties.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    }
    else if (option === "oldest") {
        properties.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
    }

    renderProperties(properties);
});

// Logout
document.getElementById("logoutBtn").onclick = () => {
    localStorage.clear();
    window.location.href = "login.html";
};
