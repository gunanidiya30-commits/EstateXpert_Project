// Get saved user data from localStorage
const user = JSON.parse(localStorage.getItem("user"));

if (!user) {
    // If no user logged in → redirect to login
    window.location.href = "login.html";
}

// Display user's name
document.getElementById("userName").innerText = user.name;

// Logout
document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("user");
    window.location.href = "login.html";
});
