// -----------------------------
// GET LOGGED-IN USER
// -----------------------------
const user = JSON.parse(localStorage.getItem("user"));

if (!user) {
  alert("Please login first");
  window.location.href = "login.html";
}

// -----------------------------
// ADD PROPERTY
// -----------------------------
document.getElementById("addPropBtn").addEventListener("click", async (e) => {
  e.preventDefault(); // stop form submit

  const title = document.getElementById("propTitle").value.trim();
  const price = document.getElementById("propPrice").value.trim();
  const location = document.getElementById("propLocation").value.trim();
  const description = document.getElementById("propDescription").value.trim();
  const images = document.getElementById("propertyImage").files;
  const status = document.getElementById("propStatus");

  if (!title || !price || !location) {
    status.style.color = "red";
    status.innerText = "Please fill all required fields.";
    return;
  }

  try {
    // ✅ USE FormData (NOT JSON)
    const formData = new FormData();
    formData.append("user_id", user.id);
    formData.append("title", title);
    formData.append("price", price);
    formData.append("location", location);
    formData.append("description", description);

    // multiple images supported
    for (let i = 0; i < images.length; i++) {
      formData.append("images", images[i]);
    }

    const response = await fetch("http://127.0.0.1:5000/add_property", {
      method: "POST",
      body: formData
    });

    const result = await response.json();

    if (result.error) {
      status.style.color = "red";
      status.innerText = result.error;
      return;
    }

    status.style.color = "green";
    status.innerText = "Property added successfully!";
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
