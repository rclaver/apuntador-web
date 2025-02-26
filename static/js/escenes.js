var estat = "inici";

// Connectar-se al servidor WebSocket
const socket = io.connect("http://" + document.domain + ":" + location.port);

// Esdeveniment que es dispara quan el servidor envia una nova línia
socket.on('new_line', function(data) {
   const escena = document.getElementById("escena_actual");
   escena.innerText = data.frase;

   const mboto = document.getElementsByName("multiboto");
   if (data.estat && data.estat != estat && mboto[0]) {
      estat = data.estat;
      const img = (estat != "inici") ? "inici" : "pausa";
      mboto[0].src = "static/img/web-" + estat + ".png";
   }
});

const multiboto = document.getElementsByName('multiboto');
multiboto[0].onclick = function() {
   const img = (estat != "inici") ? "inici" : "pausa";
   multiboto[0].src = "static/img/web-" + img + ".png";
   socket.emit(estat);
};

// Envia esdeveniment "iniciar" al servidor
document.getElementById('btn_inici').onclick = function() {
   socket.emit('inici');
};

// Envia esdeveniment "gravar" al servidor
document.getElementById('btn_record').onclick = function() {
   socket.emit('record');
};

// Envia esdeveniment "pausa" al servidor
document.getElementById('btn_pausa').onclick = function() {
   socket.emit('pausa');
};

// Envia esdeveniment "parada" al servidor
document.getElementById('btn_stop').onclick = function() {
   socket.emit('stop');
};
