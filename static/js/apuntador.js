/***
 Gestiona la comunicació entre el servidor i el client
*/
var boto = "inici";

// Connectar-se al servidor WebSocket
const socket = io.connect('https://' + document.domain + ':' + location.port);

// Esdeveniment que es dispara quan el servidor envia un nou conjunt de dades
socket.on('new_line', function(data) {
   const error = document.getElementById("div_error");
   const escena = document.getElementById("escena_actual");
   const audio = document.getElementById("audio");
   escena.innerText = data.frase;
   audio.src = (data.audio) ? "static/tmp/temp.wav" : (data.beep) ? data.beep : "";
   if (data.estat == 'gravacio') {
      document.getElementById('bt_gravacio').click();
   }
   error.innerText = (data.error) ? data.error : error.innerText;
   if (data.error) {setTimeout(2000);}
});

const multiboto = document.getElementById('bt_multiboto');
multiboto.onclick = function() {
   const boto_actiu = boto;
   boto = (boto == "inici") ? "pausa" : "inici";
   this.src = "static/img/web-" + boto + ".png";
   socket.emit(boto_actiu);  //envia esdeveniment al servidor
};

document.getElementById('bt_stop').onclick = function() {
   boto = "inici";
   multiboto.src = "static/img/web-" + boto + ".png";
   socket.emit('stop');
};
document.getElementById('bt_anterior').onclick = function() {
   socket.emit('anterior');
};
document.getElementById('bt_seguent').onclick = function() {
   socket.emit('seguent');
};


/***
 Grava l'audio captat pel micròfon en un arxiu d'audio
*/
var gravacio = false;

if (navigator.mediaDevices) {
   navigator.mediaDevices
      .getUserMedia({audio:true})
      .then(stream => { gestorMicrofon(stream) })
      .catch((err) => {
         alert("error getUserMedia: "+ err)
      });

   function gestorMicrofon(stream) {
      const options = {
        mimeType: 'audio/webm',
        numberOfAudioChannels: 1,
        sampleRate: 16000,
      };
      rec = new MediaRecorder(stream, options);
      rec.ondataavailable = e => {
         audioChunks.push(e.data);
         if (rec.state == "inactive") {
            let blob = new Blob(audioChunks, {type: 'audio/webm'});
            sendData(blob);
         }
      }
   }

   function sendData(data) {
       var form = new FormData();
       form.append('file', data, 'static/tmp/gravacio.mp3');
       $.ajax({
           type: 'POST',
           url: '/desa-gravacio',
           data: form,
           cache: false,
           processData: false,
           contentType: false
       }).done(function(data) {
           console.log(data);
       });
   }

   bt_gravacio.onclick = e => {
       if (gravacio) {
          setTimeout(2000);
          gravacio = false;
          rec.stop();
       }else {
          document.getElementById("div_error").innerText = "iniciant gravació ...";
          gravacio = true;
          audioChunks = [];
          rec.start();
       }
   };
}
