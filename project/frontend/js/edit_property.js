const propertyId = localStorage.getItem("edit_property_id");

if (!propertyId) {
    alert("Invalid Property!");
    window.location.href = "view_properties.html";
}

// Load existing property data
fetch(`http://127.0.0.1:5000/get_properties_single/${propertyId}`)
    .then(res => res.json())
    .then(data => {
        document.getElementById("title").value = data.title;
        document.getElementById("price").value = data.price;
        document.getElementById("location").value = data.location;
        document.getElementById("description").value = data.description;
    });

// Update property
document.getElementById("editPropertyForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const updatedData = {
        title: document.getElementById("title").value,
        price: document.getElementById("price").value,
        location: document.getElementById("location").value,
        description: document.getElementById("description").value
    };

    fetch(`http://127.0.0.1:5000/update_property/${propertyId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedData)
    })
        .then(res => res.json())
        .then(data => {
            alert("Property updated successfully!");
            window.location.href = "view_properties.html";
        });
});
