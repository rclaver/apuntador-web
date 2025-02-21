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

    <form class="formulari" method="post" action="apuntador.tpl">
      <legend >Selecció d'escenes</legend><br>
      <select name="seleccio_escenes" id="seleccio_escenes" size=9>
        <option value="sencer">obra sencera</option>
        <option value="joan">Joan</option>
        <option value="gisela">Gisela</option>
        <option value="canut">Canut</option>
        <option value="emma">Emma</option>
        <option value="mar">Mar</option>
        <option value="justa">Justa</option>
        <option value="tina">Tina</option>
        <option value="pompeu">Pompeu</option>
      </select>
      <p><input type="submit" name="enviar" value="enviar"></p>
    </form>
  </div>
</body>
