const propertyId = localStorage.getItem("details_id");

if (!propertyId) {
    alert("No property selected");
    window.location.href = "view_properties.html";
}

let propertyData = null;

fetch(`http://127.0.0.1:5000/property/${propertyId}`)
    .then(res => res.json())
    .then(data => {
    document.getElementById("title").innerText = data.title;
    document.getElementById("price").innerText = data.price;
    document.getElementById("location").innerText = data.location;
    document.getElementById("description").innerText = data.description;
})
    .catch(err => {
        console.error("Error fetching property details:", err);
    });

