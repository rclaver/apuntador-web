// Connexió al servidor WebSocket
const socket = io.connect('http://' + document.domain + ':' + location.port);

// Evento cuando el servidor envía una nueva lí­nea
socket.on('new_line', function(data) {
   const contenedor = document.getElementById("escena_actual");
   contenedor.innerText = data.frase;
});

// Enviar evento de "iniciar" al servidor
document.getElementById('btn_inici').onclick = function() {
   socket.emit('inici');
};

// Enviar evento de "pausar" al servidor
document.getElementById('btn_pausa').onclick = function() {
   socket.emit('pausa');
};

// Enviar evento de "detener" al servidor
document.getElementById('btn_stop').onclick = function() {
   socket.emit('stop');
};
