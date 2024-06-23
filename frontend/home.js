/* -------------------------------------   Crear Usuarios   ------------------------------------------*/
document.getElementById("userForm").addEventListener("submit", function(event) {
    event.preventDefault();

    var identificacion = document.getElementById("identificacion").value;
    var nombre = document.getElementById("nombre").value;
    var apellidos = document.getElementById("apellidos").value;
    var email = document.getElementById("email").value;
    var telefono = document.getElementById("telefono").value;

    var userData = {
        identificacion:identificacion,
        nombre: nombre,
        apellidos: apellidos,
        email: email,
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
            document.getElementById("identificacion").value = "";
            document.getElementById("nombre").value = "";
            document.getElementById("apellidos").value = "";
            document.getElementById("email").value = "";
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

/* -------------------------------------   Crear partida  ------------------------------------------*/

document.getElementById("partidaForm").addEventListener("submit", function(event) {
    event.preventDefault();

    var identificacionBuscar = document.getElementById("identificacionBuscar").value;
    var fecha = document.getElementById("fecha").value;
    var nit = document.getElementById("nit").value;
    var nombreComercio = document.getElementById("nombreComercio").value;
    var itemDescripcion = document.getElementById("itemDescripcion").value;
    var subtotal = document.getElementById("subtotal").value;
    var total = document.getElementById("total").value;
    var codigo = document.getElementById("codigo").value;

    var userData = {
        identificacionBuscar: identificacionBuscar,
        fecha: fecha,
        nit: nit,
        nombreComercio: nombreComercio,
        itemDescripcion: itemDescripcion,
        subtotal: subtotal,
        total: total,
        codigo: codigo
    };

    fetch("http://localhost:5000/partida_create", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())  // Convertir la respuesta a JSON
    .then(data => {
        if (data.error) {
            alert("Hubo un error al crear la partida: " + data.error);
        } else {
            alert("Partida creada correctamente");
            document.getElementById("partidaForm").reset();
        }
    })
    .catch(error => {
        console.error("Error al realizar la solicitud:", error);
        alert("Hubo un error al crear la partida");
    });
});

/* -------------------------------------   Consulta partidas  ------------------------------------------*/

document.getElementById('consultaForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const identificacionCliente = document.getElementById('identificacionCliente').value;

    const url = `http://localhost:5000/partidas/${identificacionCliente}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud.');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            // Limpiar la tabla
            const tbody = document.getElementById('partidasTable').querySelector('tbody');
            tbody.innerHTML = '';

            // Agregar filas a la tabla
            data.partidas.forEach(partida => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${partida.fecha}</td>
                    <td>${partida.nit}</td>
                    <td>${partida.nombreComercio}</td>
                    <td>${partida.itemDescripcion}</td>
                    <td>${partida.subtotal}</td>
                    <td>${partida.total}</td>
                    <td>${partida.codigo}</td>
                `;
                tbody.appendChild(row);
            });
            // Actualizar el total de partidas
            document.getElementById('totalPartidas').textContent = data.total_partidas;
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
            alert('Ocurrió un error al consultar las partidas fiscales.');
        });
});



