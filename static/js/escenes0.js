const contenidorEscena = document.getElementById('escena_actual');
async function actualitzaEscena() {
   const response = await fetch('/inici');
   const reader = response.body.getReader();
   const decoder = new TextDecoder();

   while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const linia = decoder.decode(value);
      contenidorEscena.innerHTML = linia;
   }
}
actualitzaEscena();