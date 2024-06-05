document.addEventListener("DOMContentLoaded", function() {
    // Lógica para cargar y mostrar la lista de facturas
    fetch("http://localhost:5000/get_users")
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener la lista');
            }
            return response.json();
        })
        .then(users => {
            var userList = document.getElementById("userList");
            userList.innerHTML = ""; // Limpiar la lista antes de agregar datos

            users.forEach(user => {
                var userItem = document.createElement("div");
                userItem.textContent = `Nombre: ${user.nombre}, Apellido: ${user.apellido}, Teléfono: ${user.telefono}`;
                userList.appendChild(userItem);
            });
        })
        .catch(error => {
            console.error("Error al cargar la lista", error);
        });
});
