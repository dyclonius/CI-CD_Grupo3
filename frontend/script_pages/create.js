document.getElementById("userForm").addEventListener("submit", function(event) {
    event.preventDefault();

    var nombre = document.getElementById("nombre").value;
    var apellido = document.getElementById("apellido").value;
    var telefono = document.getElementById("telefono").value;

    var userData = {
        nombre: nombre,
        apellido: apellido,
        telefono: telefono
    };

    fetch("http://localhost:5000/create_user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData)
    })
    .then(response => {
        if (response.ok) {
            alert("creado correctamente");
            document.getElementById("nombre").value = "";
            document.getElementById("apellido").value = "";
            document.getElementById("telefono").value = "";
        } else {
            alert("Hubo un error al crear el usuario");
        }
    })
    .catch(error => {
        console.error("Error al realizar la solicitud:", error);
        alert("Hubo un error al crear el usuario");
    });
});
 