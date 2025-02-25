  {% include "head.tpl" %}
  <!--script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.1/socket.io.min.js"></script-->
  <script src="/static/js/socket-io.js"></script>
</head>

<body bgcolor="#FFFFFF">
  {% if sentencia is not defined %}
     {% set sentencia = "Escenes per a: " ~ actor %}
  {% endif %}
  {% if estat is not defined %}
     {% set estat = "inici" %}
  {% endif %}

  <div class="contenidor">
    <div class="titol">L'apuntador del teatre</div>
    <div id="div_error" class="error text"></div>
    <div id="escena_actual" class="escena text">{{sentencia}}</div>

    <div id="div_botons" class="div_botons contenidor">
      <img id="btn_anterior" class="imatge" onClick="window.location.href='{{ url_for('anterior', escena=actor) }}';" src="{{url_for('static', filename='img/web-anterior.png')}}">
      <img id="{{'btn_' ~ estat}}" class="imatge" src="{{url_for('static', filename='img/web-' ~ estat ~ '.png')}}">
      <img id="btn_seguent" class="imatge" onClick="window.location.href='{{ url_for('seguent', escena=actor) }}';" src="{{url_for('static', filename='img/web-seguent.png')}}">
      {% if estat == "stop" %}
      <img id="btn_pausa" class="imatge" onClick="window.location.href='{{ url_for('pausa', escena=actor) }}';" src="{{url_for('static', filename='img/web-pausa.png')}}">
      <img id="btn_record" class="imatge" onClick="window.location.href='{{ url_for('record', escena=actor) }}';" src="{{url_for('static', filename='img/web-record.png')}}">
      {% endif %}
    </div>
  </div>

  {% if estat == "ini" %}
     <script src="/static/js/escenes4.js"></script>
  {% endif %}

  <script>
      // Conectarse al servidor WebSocket
      const socket = io.connect('http://' + document.domain + ':' + location.port);

      // Evento que se dispara cuando el servidor envía una nueva línea
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
  </script>

</body>
