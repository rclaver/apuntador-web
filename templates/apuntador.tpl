{% include "head.tpl" %}
  <!--script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.1/socket.io.min.js"></script-->
  <script src="/static/js/socket-io.js"></script>
</head>

<body bgcolor="#FFFFFF">
  {% if sentencia is not defined %}
     {% set sentencia = "Escenes per a: " ~ actor %}
  {% endif %}

  <div class="contenidor">
    <div class="titol">L'apuntador del teatre</div>
    <div id="div_error" class="error text"></div>
    <div id="escena_actual" class="escena text">{{sentencia}}</div>

    <div id="div_botons" class="div_botons contenidor">
      <img id="bt_anterior" class="imatge" src="{{url_for('static', filename='img/web-anterior.png')}}">
      <img id="bt_stop" class="imatge" src="{{url_for('static', filename='img/web-stop.png')}}">
      <img id="bt_multiboto" class="imatge" src="{{url_for('static', filename='img/web-inici.png')}}">
      <img id="bt_seguent" class="imatge" src="{{url_for('static', filename='img/web-seguent.png')}}">
    </div>
    <img id="bt_gravacio" class="invisible" src="{{url_for('static', filename='img/web-gravacio.png')}}">
    <audio id="audio" autoplay preload="none" type="audio/wav">
  </div>

  <script>
      var boto = "inici";

      // Connectar-se al servidor WebSocket
      const socket = io.connect('http://' + document.domain + ':' + location.port);

      // Esdeveniment que es dispara quan el servidor envia una nova línia
      socket.on('new_line', function(data) {
         const error = document.getElementById("div_error");
         const escena = document.getElementById("escena_actual");
         const audio = document.getElementById("audio");
         escena.innerText = data.frase;
         audio.src = (data.audio) ? "static/tmp/temp.wav" : "";
         if (data.estat == 'gravacio') {
            error.innerText = "gravant ...";
            document.getElementById('bt_gravacio').click();
         }else {
            error.innerText = "";
            if (gravacio) {
               document.getElementById('bt_gravacio').click();
            }
         }
         error.innerText = (data.error) ? data.error : error.innerText;
      });

      const multiboto = document.getElementById('bt_multiboto');
      multiboto.onclick = function() {
         const boto_actiu = boto;
         boto = (boto == "inici") ? "pausa" : "inici";
         multiboto.src = "static/img/web-" + boto + ".png";
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
  </script>
  <script>
    var gravacio = false;

    navigator
        .mediaDevices
        .getUserMedia({audio: true})
        .then(stream => { gestorMicrofon(stream) });

    function gestorMicrofon(stream) {
       rec = new MediaRecorder(stream);
       rec.ondataavailable = e => {
          audioChunks.push(e.data);
          if (rec.state == "inactive") {
             let blob = new Blob(audioChunks, {type: 'audio/mpeg-3'});
             sendData(blob);
          }
       }
    }

    function sendData(data) {
        var form = new FormData();
        form.append('file', data, 'static/tmp/gravacio.mp3');
        form.append('title', 'gravacio.mp3');
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
           console.log('aturant gravació ...');
           gravacio = false;
           rec.stop();
        }else {
           console.log('iniciant gravació ...');
           gravacio = true;
           audioChunks = [];
           rec.start();
        }
    };
  </script>
</body>