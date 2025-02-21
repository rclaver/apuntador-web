<!DOCTYPE html>
<html>
<head>
  <meta name="robots" content="index,follow">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>L'apuntador del teatre</title>
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link href="csjs/estils.css" rel="stylesheet" type="text/css" />
  <script src="csjs/script.js"></script>

</head>

<body bgcolor="#FFFFFF">
  <div class="contenidor">
      <div class="titol">L'apuntador del teatre</div>
      <div id="div_error" class="error text"></div>
      <div id="escena_actual" class="escena text"></div>

      <div id="div_botons" class="div_botons contenidor">
        <img id="btn_anterior" class="imatge " src="recursos/web-anterior.png" onClick="anterior();">
        <img id="btn_play" class="imatge" src="recursos/web-play.png" onClick="play('escena');">
        <img id="btn_seguent" class="imatge" src="recursos/web-seguent.png" onClick="seguent();">
      </div>
  </div>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      var formu = formulari();
      var actor = get_parametres("seleccio_escenes");
      document.getElementById('div_error').innerHTML = 'Escenes de : "' + {{actor}} + '"';
    });
  </script>
</body>
