// Conexi√≥n al servidor WebSocket
const socket = io.connect('http://' + document.domain + ':' + location.port);

// Evento cuando el servidor env√≠a una nueva lÌ≠nea
socket.on('new_line', function(data) {
   const contenedor = document.getElementById("escena_actual");
   contenedor.innerText = data.line;  // Reemplazamos el contenido del div con la nueva l√≠nea
});

// Enviar evento de "iniciar" al servidor
document.getElementById('btn-inici').onclick = function() {
   socket.emit('start');
};

// Enviar evento de "pausar" al servidor
document.getElementById('btn-pausa').onclick = function() {
   socket.emit('pause');
};

// Enviar evento de "detener" al servidor
document.getElementById('btn-stop').onclick = function() {
   socket.emit('stop');
};
