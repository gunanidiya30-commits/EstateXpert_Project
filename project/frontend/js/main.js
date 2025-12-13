console.log("JS loaded!");
document.getElementById("loadUsersBtn").onclick = function () {
    fetch("http://127.0.0.1:5000/api/users")
        .then(response => response.json())
        .then(data => {

            let html = "";

            data.data.forEach(user => {
    html += `
        <div style="padding: 10px; background: white; margin: 5px; border-radius: 6px;">
            <b>${user.id}</b>: ${user.name} (${user.email})
            
            <button onclick="deleteUser(${user.id})" style="margin-left: 10px;">
                Delete
            </button>

            <button onclick="openEditForm(${user.id}, '${user.name}', '${user.email}', '${user.password}')"
                style="margin-left: 5px;">
                Edit
            </button>
        </div>
    `;
});


            document.getElementById("usersList").innerHTML = html;

        })
        .catch(err => {
            console.error("Error:", err);
        });
};

document.getElementById("addUserBtn").onclick = function () {
    let userData = {
        name: document.getElementById("nameInput").value,
        email: document.getElementById("emailInput").value,
        password: document.getElementById("passwordInput").value
    };

    fetch("http://127.0.0.1:5000/api/users/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData)
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("addUserStatus").innerHTML =
                data.message;

            // refresh users after adding
            document.getElementById("loadUsersBtn").click();
        })
        .catch(err => {
            console.error("Error:", err);
        });
};


function deleteUser(id) {
    fetch(`http://127.0.0.1:5000/api/users/delete/${id}`, {
        method: "DELETE"
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            document.getElementById("loadUsersBtn").click(); // refresh
        })
        .catch(err => console.error("Error:", err));
}

function openEditForm(id, name, email, password) {
    window.editingUserId = id;

    document.getElementById("editName").value = name;
    document.getElementById("editEmail").value = email;
    document.getElementById("editPassword").value = password;
}

document.getElementById("saveUserBtn").onclick = function () {
    let userData = {
        name: document.getElementById("editName").value,
        email: document.getElementById("editEmail").value,
        password: document.getElementById("editPassword").value
    };

    fetch(`http://127.0.0.1:5000/api/users/update/${window.editingUserId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData)
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("editUserStatus").innerHTML = data.message;
            document.getElementById("loadUsersBtn").click(); // refresh list
        })
        .catch(err => console.error("Error:", err));
};
