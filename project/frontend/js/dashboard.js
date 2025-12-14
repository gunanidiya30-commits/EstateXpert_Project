const user = JSON.parse(localStorage.getItem("user"));
document.getElementById("userName").innerText = user.name;

// Load properties
async function loadProperties() {
    let response = await fetch(`http://127.0.0.1:5000/get_properties/${user.id}`);
    let data = await response.json();

    let container = document.getElementById("propertyList");
    container.innerHTML = "";

    data.properties.forEach(prop => {
        container.innerHTML += `
            <div class="property-card">
                <h3>${prop.title}</h3>
                <p class="price">₹${prop.price}</p>
                <p><b>Location:</b> ${prop.location}</p>
                <p>${prop.description}</p>
            </div>
        `;
    });
}

loadProperties();

// DELETE PROPERTY
async function deleteProperty(id) {
    const confirmDelete = confirm("Are you sure you want to delete this property?");
    if (!confirmDelete) return;

    let response = await fetch(`http://127.0.0.1:5000/delete_property/${id}`, {
        method: "DELETE"
    });

    let result = await response.json();
    alert(result.message);
    loadProperties();
}

// EDIT (Day‑8)
function editProperty(id) {
    alert("Edit feature coming in Day‑8!");
}
