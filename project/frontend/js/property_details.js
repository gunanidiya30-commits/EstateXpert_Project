document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const propertyId = params.get("id");

    if (!propertyId) {
        alert("Property ID missing");
        return;
    }

    fetch(`http://127.0.0.1:5000/get_property/${propertyId}`)
        .then(response => response.json())
        .then(property => {
            if (property.error) {
                alert(property.error);
                return;
            }

            document.getElementById("title").innerText = property.title;
            document.getElementById("price").innerText = "₹ " + property.price;
            document.getElementById("location").innerText = property.location;
            document.getElementById("description").innerText = property.description;

            // ✅ IMAGE GALLERY
            const gallery = document.getElementById("imageGallery");

            if (property.images && property.images.length > 0) {
                property.images.forEach(img => {
                    const imageEl = document.createElement("img");
                    imageEl.src = `http://127.0.0.1:5000${img}`;

                    imageEl.classList.add("detail-image");
                    gallery.appendChild(imageEl);
                });
            }
        })
        .catch(error => {
            console.error("Error fetching property:", error);
        });
});
