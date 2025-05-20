let data = {
    // Inicializa con valores por defecto, pero se sobrescribirán con los del ESP32
    "temperature": {
        "actual_value": 0,
        "minimum": 0,
        "maximum": 0
    },
    "humidity": {
        "actual_value": 0,
        "minimum": 0,
        "maximum": 0
    },
    "light": {
        "actual_value": 0,
        "minimum": 0,
        "maximum": 0
    },
    "relays": {
        "relay01": 0,
        "relay02": 0
    }
};

function actualizarDatos() {
    fetch('http://192.168.1.111/api/datos')
      .then(response => {
          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
      })
      .then(espData => { // Cambiado 'data' a 'espData' para evitar conflicto con la global 'data'
        // Actualiza los valores de los sensores y relevadores
        document.getElementById('temperatura').textContent = espData.temperature.actual_value + " °C"; // Añadido unidad
        document.getElementById('humedad').textContent = espData.humidity.actual_value + " %";       // Añadido unidad
        document.getElementById('luz').textContent = espData.light.actual_value + " lux";          // Añadido unidad
        document.getElementById('relevador01').textContent = espData.relays.relay01 ? "Encendido" : "Apagado";
        document.getElementById('relevador02').textContent = espData.relays.relay02 ? "Encendido" : "Apagado";

        // *** IMPORTANTE: Actualizar la variable 'data' global con los umbrales del ESP32 ***
        data.temperature.minimum = espData.temperature.minimum;
        data.temperature.maximum = espData.temperature.maximum;
        data.humidity.minimum = espData.humidity.minimum;
        data.humidity.maximum = espData.humidity.maximum;
        data.light.minimum = espData.light.minimum;
        data.light.maximum = espData.light.maximum;
        // Los valores actuales también se pueden actualizar en la global si quieres, aunque se usan directamente arriba.
        data.temperature.actual_value = espData.temperature.actual_value;
        data.humidity.actual_value = espData.humidity.actual_value;
        data.light.actual_value = espData.light.actual_value;
        data.relays.relay01 = espData.relays.relay01;
        data.relays.relay02 = espData.relays.relay02;


        // Ahora sí, llamar a llenarTablaParametros DESPUÉS de que 'data' global esté actualizada
        llenarTablaParametros(); 
      })
      .catch(error => {
        console.error('Error al obtener datos:', error);
        // Opcional: mostrar un mensaje en la interfaz de usuario si hay un error
        document.getElementById('temperatura').textContent = "Error";
        document.getElementById('humedad').textContent = "Error";
        document.getElementById('luz').textContent = "Error";
        document.getElementById('relevador01').textContent = "Error";
        document.getElementById('relevador02').textContent = "Error";
        // También limpiar o mostrar error en la tabla de parámetros
        const tbody = document.getElementById("tbl-body");
        tbody.innerHTML = `<tr><td colspan="3">Error al cargar parámetros</td></tr>`;
      });
}

function llenarTablaParametros() {
    const tbody = document.getElementById("tbl-body");
    tbody.innerHTML = ""; // Limpiar el contenido actual de la tabla

    // Crear filas para la tabla usando la variable 'data' global (que ya se actualizó con el fetch)
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
 
// Actualizar automáticamente cada cierto tiempo
setInterval(actualizarDatos, 10000); // Cada 10 segundos