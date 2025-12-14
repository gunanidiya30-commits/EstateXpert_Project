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

    if (data.length === 0) {
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
            </div>
        `;
        container.innerHTML += card;
    });
}

// Load on page start
loadProperties();

// Logout
document.getElementById("logoutBtn").onclick = () => {
    localStorage.clear();
    window.location.href = "login.html";
};
