

let counter = 0; // Contador para el número de clics

let data = {
    "temperature": {
        "actual_value": 25,
        "minimum": 0,
        "maximum": 50
    },
    "humidity": {
        "actual_value": 60,
        "minimum": 20,
        "maximum": 90
    },
    "light": {
        "actual_value": 300,
        "minimum": 0,
        "maximum": 1000
    },
    "relays": {
        "relay01": 0,
        "relay02": 1
    }
}

function actualizarDatos() {
    //fetch('/api/estado')
    //  .then(response => response.json())
    //  .then(data => {
    //    document.getElementById('temperatura').textContent = data.temperatura;
    //    document.getElementById('humedad').textContent = data.humedad;
    //    document.getElementById('luz').textContent = data.luz;
    //    document.getElementById('relevador01').textContent = data.estado_relevador01 ? "Encendido" : "Apagado";
    //    document.getElementById('relevador02').textContent = data.estado_relevador02 ? "Encendido" : "Apagado";
    //  })
    //  .catch(error => {
    //    console.error('Error al obtener datos:', error);
    //  });
    console.log("Actualizando datos...");
    document.getElementById('temperatura').textContent = data.temperature.actual_value + counter;
    document.getElementById('humedad').textContent = data.humidity.actual_value + counter;
    document.getElementById('luz').textContent = data.light.actual_value + counter;
    document.getElementById('relevador01').textContent = data.relays.relay01 == 0 ? "apagado" : "encendido";    
    document.getElementById('relevador02').textContent = data.relays.relay02 == 0 ? "apagado" : "encendido";

    // Actualizar la tabla de parámetros
    llenarTablaParametros();

    counter++;
}


function llenarTablaParametros() {
    const tbody = document.getElementById("tbl-body");
    tbody.innerHTML = ""; // Limpiar el contenido actual de la tabla

    // Crear filas para la tabla
    const row1 = document.createElement("tr");
    row1.innerHTML = `
        <td>Temperatura</td>
        <td>${data.temperature.minimum}</td>
        <td>${data.temperature.maximum}</td>
    `;

    const row2 = document.createElement("tr");
    row2.innerHTML = `
        <td>Humedad</td>
        <td>${data.humidity.minimum}</td>
        <td>${data.humidity.maximum}</td>
    `;

    const row3 = document.createElement("tr");
    row3.innerHTML = `
        <td>Luz</td>
        <td>${data.light.minimum}</td>
        <td>${data.light.maximum}</td>
    `;

    // Agregar filas al cuerpo de la tabla
    tbody.appendChild(row1);
    tbody.appendChild(row2);
    tbody.appendChild(row3);
}

// Cuando la página haya cargado, actualizamos los datos automáticamente
window.onload = actualizarDatos;
  
// Opcionalmente: actualizar automáticamente cada cierto tiempo
setInterval(actualizarDatos, 10000); // Cada 5 segundos
  