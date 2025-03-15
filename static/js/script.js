function formulari() {
   var error, s_escena, i;
   s_escena = document.getElementById("seleccio_escenes");
   i = s_escena.selectedIndex;
   escena = s_escena.options[i].value;
   form = document.getElementById("formulari");
   form.value=escena;
   form.submit();
}
