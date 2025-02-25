$(document).ready(function() {
   let contenedor = $("#escena_actual");

   function getLine() {
      $.ajax({
         url: '/inici',  // Ruta para obtener las líneas
         success: function(data) {
            contenedor.text(data);  // Reemplazamos el contenido del div
         },
         error: function() {
            console.log("Error al obtener la línea.");
         }
      });
   }

   // Llamar a la función para obtener una línea cada 1 segundo
   setInterval(getLine, 1000);
});
