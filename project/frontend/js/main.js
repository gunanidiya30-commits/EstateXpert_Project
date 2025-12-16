// main.js — GLOBAL SESSION HANDLER

if (!localStorage.getItem("user")) {
    // not logged in
    if (!window.location.href.includes("login.html") &&
        !window.location.href.includes("signup.html")) {
        window.location.href = "login.html";
    }
} else {
    window.user = JSON.parse(localStorage.getItem("user"));
}
