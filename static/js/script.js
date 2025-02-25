var escena;

function formulari() {
   var error, s_escena, i;
   s_escena = document.getElementById("seleccio_escenes");
   i = s_escena.selectedIndex;
   escena = s_escena.options[i].value;
   form = document.getElementById("formulari");
   form.value=escena;
   form.submit();
}

function play(escena) {
   var xhr;
   var contenidoRecibido = '';

   if (escena.length===0) {
      document.getElementById("escena_actual").innerHTML = "";
      return;
   }

   xhr = new XMLHttpRequest();

   xhr.onreadystatechange = function() {
      if (xhr.readyState===4 && xhr.status===200) {
         contenidoRecibido = xhr.responseText;
         document.getElementById("escena_actual").innerHTML = contenidoRecibido;
      }
   };

   xhr.open("POST","apuntador.py?escena="+escena);
   xhr.send();
}

function anterior() {
}

function seguent() {
}

function get_parametres(param) {
   let params = new URLSearchParams(document.location.search);
   let value = params.get(param);
   return value;
}

function visible(e, es_visible) {
   let d = ((es_visible) ? "block" : "none");
   let v = ((es_visible) ? "visible" : "hidden");
   document.getElementById(e).style.display = d;
   document.getElementById(e).style.visibility = v;
}

function get_propietat(e) {
   return "weight: " + document.getElementById(e).style.fontWeight + ".";
}

function get_screen_sizes(selection) {
   var sizes;
   if (selection === "min") {
      sizes = "- body.clientHeight: " + document.body.clientHeight + "<br>" +
              "- window.screen.height: " + window.screen.height + "<br>" +
              "- window.innerHeight: " + window.innerHeight + "<br>" +
              "- body.clientWidth: " + document.body.clientWidth + "<br>" +
              "- window.screen.width: " + window.screen.width + "<br>" +
              "- window.innerWidth: " + window.innerWidth;
   }else {
      sizes = "- body.scrollHeight: " + document.body.scrollHeight + "<br>" +
              "- documentElement.scrollHeight: " + document.documentElement.scrollHeight + "<br>" +
              "- body.offsetHeight: " + document.body.offsetHeight + "<br>" +
              "- documentElement.offsetHeight: " + document.documentElement.offsetHeight + "<br>" +
              "- body.clientHeight: " + document.body.clientHeight + "<br>" +
              "- documentElement.clientHeight: " + document.documentElement.clientHeight + "<br>" +
              "- body.scrollWidth: " + document.body.scrollWidth + "<br>" +
              "- documentElement.scrollWidth: " + document.documentElement.scrollWidth + "<br>" +
              "- body.offsetWidth: " + document.body.offsetWidth + "<br>" +
              "- documentElement.offsetWidth: " + document.documentElement.offsetWidth + "<br>" +
              "- body.clientWidth: " + document.body.clientWidth + "<br>" +
              "- documentElement.clientWidth: " + document.documentElement.clientWidth;
   }
   return sizes;
}