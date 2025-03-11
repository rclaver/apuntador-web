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
    <audio autoplay>
       <source src="{{ url_for('static', filename='tmp/temp.wav') }}" type="audio/wav">
    </audio>
  </div>

  <script>
      var boto = "inici";

      // Connectar-se al servidor WebSocket
      const socket = io.connect('http://' + document.domain + ':' + location.port);

      // Esdeveniment que es dispara quan el servidor envia una nova línia
      socket.on('new_line', function(data) {
         const error = document.getElementById("div_error");
         const escena = document.getElementById("escena_actual");
         escena.innerText = data.frase;
         error.innerText = (data.estat == 'record') ? "gravant ..." : "";
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

</body>