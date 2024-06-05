function loadContent(page) {
    fetch(page + ".html")
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar el contenido');
            }
            return response.text();
        })
        .then(html => {
            document.body.innerHTML = html;
            if (page !== "index") {
                loadScript(page);
            }
        })
        .catch(error => {
            console.error("Error al cargar el contenido:", error);
        });
}

function loadScript(page) {
    var script = document.createElement("script");
    script.src = page + ".js";
    document.body.appendChild(script);
}

document.addEventListener("DOMContentLoaded", function() {
    loadContent("index");
});



