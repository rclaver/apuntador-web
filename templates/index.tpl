<!DOCTYPE html>
<html>
<head>
  <meta name="robots" content="index,follow">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>L'apuntador del teatre</title>
  <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />
  <link rel="stylesheet" type="text/css" href="/static/css/estils.css" />
  <script src="/static/js/script.js"></script>
</head>

<body bgcolor="#FFFFFF">
  <div class="contenidor">
    <div class="titol">L'apuntador del teatre</div>
    <form id="formulari" class="formulari" method="post" onClick="formulari();" action="apuntador">
      <div id="div_seleccio_escenes">
        <legend>Selecció d'escenes {{escena}}</legend>
        <select name="seleccio_escenes" id="seleccio_escenes" size=11>
          <optgroup label="actors">
            <option value="canut">Canut</option>
            <option value="emma">Emma</option>
            <option value="gisela">Gisela</option>
            <option value="joan">Joan</option>
            <option value="justa">Justa</option>
            <option value="mar">Mar</option>
            <option value="pompeu">Pompeu</option>
            <option value="tina">Tina</option>
          <optgroup label="----------------">
            <option value="sencer">obra sencera</option>
        </select>
      </div>
    </form>
  </div>
</body>
