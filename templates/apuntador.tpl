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
      <img id="bt_inici" name="multiboto" class="imatge" src="{{url_for('static', filename='img/web-inici.png')}}">
      <img id="bt_record" class="imatge" src="{{url_for('static', filename='img/web-record.png')}}">
      <img id="bt_seguent" class="imatge" src="{{url_for('static', filename='img/web-seguent.png')}}">
    </div>
  </div>

  <script>
      var estat = "inici";

      // Connectar-se al servidor WebSocket
      const socket = io.connect('http://' + document.domain + ':' + location.port);

      // Esdeveniment que es dispara quan el servidor envia una nova línia
      socket.on('new_line', function(data) {
         const escena = document.getElementById("escena_actual");
         escena.innerText = data.frase;
      });

      const multiboto = document.getElementsByName('multiboto');
      multiboto[0].onclick = function() {
         const estat_actiu = estat;
         estat = (estat == "inici") ? "pausa" : "inici";
         multiboto[0].src = "static/img/web-" + estat + ".png";
         socket.emit(estat_actiu);
      };

      document.getElementById('bt_record').onclick = function() {
         // Envia esdeveniment al servidor
         socket.emit('record');
      };
      document.getElementById('bt_stop').onclick = function() {
         socket.emit('stop');
      };
  </script>

</body>
