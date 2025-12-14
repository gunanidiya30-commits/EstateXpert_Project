// READ USER FROM LOCAL STORAGE SAFELY
const user = JSON.parse(localStorage.getItem("user"));

if (!user) {
    alert("Please login first!");
    window.location.href = "login.html";
} else {
    document.getElementById("userName").innerText = user.name;
}

// LOAD PROPERTIES
async function loadProperties() {
    let response = await fetch(`http://127.0.0.1:5000/get_properties/${user.id}`);
    let data = await response.json();

    let container = document.getElementById("propertyList");
    container.innerHTML = "";

    data.forEach(prop => {
        container.innerHTML += `
            <div class="property-card">
                <h3>${prop.title}</h3>
                <p class="price">₹${prop.price}</p>
                <p><b>Location:</b> ${prop.location}</p>
                <p>${prop.description}</p>

                <button class="btn-delete" onclick="deleteProperty(${prop.id})">
                    Delete
                </button>
            </div>
        `;
    });
}

loadProperties();


// DELETE PROPERTY
async function deleteProperty(id) {
    const confirmation = confirm("Are you sure you want to delete this property?");
    if (!confirmation) return;

    let response = await fetch(`http://127.0.0.1:5000/delete_property/${id}`, {
        method: "DELETE"
    });

    let result = await response.json();
    alert(result.message);

    loadProperties();  // refresh UI
}


// LOGOUT
document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("user");
    window.location.href = "login.html";
});
