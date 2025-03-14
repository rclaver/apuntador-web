#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 16:32:05 2025
@author: rafael

pip install flask flask-socketio
pip install -r requirements.txt

Las aplicaciones Python con Flask deben ejecutarse desde una terminal.
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.

Ejecutar en la nube:
- subir el repositorio a Github
- crear una aplicación en dashboard.render.com
"""
import os, re, time, glob
import difflib
import threading

from flask import Flask, render_template, request, redirect, flash
from flask_socketio import SocketIO
#from dotenv import load_dotenv

from gtts import gTTS
import soundfile as sf

import pyaudio
import wave

import pyworld as pw
from pydub import AudioSegment
from pydub.playback import play

import speech_recognition as sr

# -----------------
# variables globals
#
C_NONE="\033[0m"
CB_YLW="\033[1;33m"
CB_BLU="\033[1;34m"

titol = "casats"
actor = ""
estat = "inici"
fil = None
en_pausa = False
en_grabacio = False
stop = False

pattern_person = "^(\w*?\s?)(:\s?)(.*$)"
pattern_narrador = "([^\(]*)(\(.*?\))(.*)"

dir_dades = "dades"
dir_recursos = "static/img"
base_arxiu_text = titol
tmp3 = "static/tmp/temp.mp3"
twav = "static/tmp/temp.wav"
gmp3 = "static/tmp/gravacio.mp3"
gwav = "static/tmp/gravacio.wav"
beep = f"{dir_recursos}/beep.wav"
beep_error = f"{dir_recursos}/error.wav"

pendent_escolta = False  #indica si ha arribat el moment d'escoltar l'actor
audio_pendent = None

Personatges = {'Joan':   {'speed': 1.20, 'grave': 3.6, 'reduction': 0.6},
               'Gisela': {'speed': 1.30, 'grave': 0.9, 'reduction': 1.7},
               'Mar':    {'speed': 1.40, 'grave': 0.6, 'reduction': 1.4},
               'Emma':   {'speed': 1.40, 'grave': 0.7, 'reduction': 1.0},
               'Tina':   {'speed': 1.30, 'grave': 1.1, 'reduction': 1.0},
               'Justa':  {'speed': 1.40, 'grave': 1.8, 'reduction': 0.9},
               'Pompeu': {'speed': 1.40, 'grave': 2.2, 'reduction': 0.9},
               'Canut':  {'speed': 1.50, 'grave': 2.0, 'reduction': 1.0}}
Narrador = {'speed': 1.22, 'grave': 1.6, 'reduction': 1.7}
Narrador = "narrador"

def crear_app():
   app = Flask(__name__) #instancia de Flask
   socketio = SocketIO(app)
   key_secret = os.getenv("API_KEY")

   @app.route("/")
   def index():
      return render_template("index.tpl")

   @app.route("/apuntador", methods = ["GET", "POST"])
   def apuntador():
      global actor
      if request.method == "POST":
         actor = request.form.get("seleccio_escenes")
      if actor:
         return render_template("apuntador.tpl", actor=actor)
      else:
         return render_template("index.tpl")

   @app.route('/desa-gravacio', methods=['POST'])
   def desa_gravacio():
      if 'file' not in request.files:
         flash('No hi ha element file')
         return redirect(request.url)
      if request.files['file'].filename == '':
         flash('No has seleccionat cap fitxer')
         return redirect(request.url)

      print(f"{CB_BLU}desa_gravacio:{C_NONE}", request.files['file'].filename, end="\n\n")
      file = request.files['file']
      file.save(file.filename)
      return file.filename


   '''
   Espera 1 segon per rebre la gravació feta en el client
   '''
   def espera_gravacio(arxiu):
      c = 0
      while not os.path.exists(arxiu) and c <= 20:
         time.sleep(0.1)
         c += 1
         print(f"espera gravacio: {c}")
      return os.path.exists(arxiu)

   def espera(l):
      c = 0
      while c <= l:
         time.sleep(0.1)
         c += 1

   '''
   Compara 2 textos i indica el percentatge de semblances
   '''
   def ComparaSekuenciesDeText(text_1, text_2):
      # normalitza el text original
      replace = "[.,!¡¿?()]"
      while re.search(replace, text_1):
         for r in replace:
            text_1 = text_1.replace(r, " ")
      text_1 = re.sub("\s+", " ", text_1).lower()
      encert = difflib.SequenceMatcher(None, text_1, text_2).ratio() * 100
      return encert

   def codifica_html(text):
      cerca = "ÀÈÉÍÒÓÚàèéíòóú"
      subs = ["&Agrave;","&Egrave;","&Eacute;","&Iacute;","&Ograve;","&Oacute;","&Uacute;","&agrave;","&egrave;","&eacute;","&iacute;","&ograve;","&oacute;","&uacute;"]
      i = 0
      for s in cerca:
         text.replace(s, subs[i])
         i += 1
      return text

   '''
   Transforma un audio en text (utilitza speech_recognition)
   @type audio: AudioSource; audio d'entrada que es vol convertir a text
   @type r: Recognizer; instància de speech_recognition.Recognizer()
   '''
   def reconeixement_d_audio(audio, r):
      text_reconegut = ""
      try:
         # Google Speech Recognition. For testing purposes, we're just using the default API key
         # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
         text_reconegut = r.recognize_google(audio, language="ca")
         print(f"- {text_reconegut}")
      except sr.UnknownValueError:
         print("No he sentit res")
      except sr.RequestError as e:
         print("Could not request results from Google Speech Recognition service; {0}".format(e))

      return text_reconegut

   '''
   Genera un arxiu de text a partir d'un arxiu d'audio
   @type warxiu: string; nom del fitxer wav del que es vol extraure el text
   '''
   def audio_a_text(warxiu):
      r = sr.Recognizer()
      with sr.AudioFile(warxiu) as source:
         audio = r.record(source)  # llegeix l'arxiu d'audio sencer

      text_reconegut = reconeixement_d_audio(audio, r)
      return text_reconegut

   '''
   Mostra el text que s'està processant.
   '''
   def mostra_sentencia(text, ends):
      text = codifica_html(text) + ends
      return text

   '''
   Genera l'arxiu d'audio corresponent al text
   @type text: string; text que es vol convertir en veu
   @type veu_params: llsta; llista de paràmetres de veu del personatge a tractar
   @type ends: string; marca de final de la instrucció print
                       (": ") indica que el paràmetre text és el nom del personatge
   '''
   def text_a_audio(text, veu_params, ends):
      global audio_pendent
      # Si ends == ": " significa que text és el nom del personatge, per tant, no es genera audio
      # Si veu_params == "narrador" no es genera audio
      if ends != ": " and veu_params != "narrador":
          # obtenir els parametres
          speed, grave, reduction = list(veu_params.values())

          # Generar un arxiu d'audio temporal amb gTTS
          tts = gTTS(text, lang='ca')
          tts.save(tmp3)

          # Convertir l'objecte mp3 a wav
          audio = AudioSegment.from_mp3(tmp3)
          audio.export(twav, format="wav")

          # tractament de l'audio
          data, samplerate = sf.read(twav)
          f0, sp, ap = pw.wav2world(data, samplerate)
          yy = pw.synthesize(f0/grave, sp/reduction, ap, samplerate/speed, pw.default_frame_period)
          sf.write(twav, yy, samplerate)
          audio_pendent = AudioSegment.from_wav(twav)

      return mostra_sentencia(text, ends)

   '''
   Grava en viu la veu de l'actor, genera el text corresponent i el compara amb el text que li correspon
   @type text: string; text que es vol gravar
   '''
   def escolta_actor(text, ends):
      global actor, audio_pendent
      print(f"{CB_BLU}escolta_actor: {CB_YLW}{text}{C_NONE}")
      if espera_gravacio(gmp3):
         # Convertir l'objecte mp3 a wav
         try:
            print(f"{CB_BLU}Convertir l'objecte mp3 a wav{C_NONE}")
            audio = AudioSegment.from_mp3(gmp3)
            audio.export(gwav, format="wav")
            nou_text = audio_a_text(gwav)
            print(f"{CB_BLU}nou_text: {CB_YLW}{nou_text}{C_NONE}")
         except:
            nou_text = None
         os.remove(gmp3)
      encert = 0
      if 'nou_text' in locals() and nou_text:
         encert = ComparaSekuenciesDeText(text, nou_text)
      if encert < 90:
         print(f"encert: {encert}%", " ")
         socketio.emit('new_line', {'frase':"", 'error':f"No ho he entès bé: {encert}%", 'beep':beep_error})  # Enviar la línia al client
         ret = text_a_audio(text, Personatges[actor.capitalize()], ends)
      else:
         ret = mostra_sentencia(text, ends)

      return ret

   '''
   S'atura el thread mentre dura la gabacio
   '''
   def en_process_de_grabacio(ret):
      global en_grabacio
      if en_grabacio or pendent_escolta:
         print(f"{CB_BLU}en_process_de_grabacio{C_NONE}", ret)
         socketio.emit('new_line', {'frase':ret, 'estat':"gravacio", 'beep':beep})  # Enviar el text al client
         #espera(len(ret)/10)
         #socketio.emit('new_line', {'frase':"", 'estat':"gravacio"})  # Enviar el text al client
      en_grabacio = False

   """
   Parteix la sentència en fragments que puguin ser processats per gTTs
   @type text: string; text que es tracta
   @type to_veu: list; paràmetres de veu
   @type ends: string; caracter de finalització de la funció print
   """
   def processa_fragment(text, escena, to_veu, ends):
      global pendent_escolta, en_grabacio
      ret = ""
      long_text = len(text)
      ini = 0
      while ini < long_text:
         long_max = 600
         if long_max < long_text:
            long_max = text[ini:].find(" ", long_max)
         if long_max == -1 or long_max > long_text:
            long_max = long_text
         text = text[ini:ini+long_max]

         if text.lower() == actor.lower():
            pendent_escolta = True
            ret = mostra_sentencia(text, ends)
            print(f"{CB_BLU}pendent_escolta = True:{C_NONE}", ret)
         elif pendent_escolta == True:
            en_process_de_grabacio(text)
            ret = escolta_actor(text, ends)
            print(f"{CB_BLU}pendent_escolta = False:{C_NONE}", ret, end="")
            pendent_escolta = False
            break
         else:
            ret += text_a_audio(text, to_veu, ends)

         ini += long_max

      return ret

   '''
   Lectura del text sencer o de l'escena seleccionada de l'obra
   Partició del text en sentències (una sentència correspón a una línia del text)
   Cada sentència pot pertanyer, bé al narrador, bé a un personatge
   '''
   def processa_escena(arxiu_escena="", i=0, n_escenes=0):
      global stop, en_pausa, en_grabacio, audio_pendent
      escena = f"_{arxiu_escena}_" if arxiu_escena else "_"
      print(f"{CB_YLW}arxiu_escena: {arxiu_escena}{C_NONE}")
      if not os.path.isfile(arxiu_escena):
         arxiu_escena = f"{dir_dades}/{base_arxiu_text}.txt"

      with open(arxiu_escena, 'r', encoding="utf-8") as f:
         sentencies = f.read().split('\n')

      for sentencia in sentencies:
         ret = ""
         audio_pendent = None
         if sentencia:
            # extraure el personatje ma(1) i el text ma(3)
            ma = re.match(pattern_person, sentencia)
            if ma:
               personatje = ma.group(1)
               ret = processa_fragment(personatje, escena, Narrador, ": ")

               to_veu = Personatges[personatje] if personatje in Personatges else Narrador
               # extraure, del text ma(3), els comentaris del narrador
               mb = re.match(pattern_narrador, ma.group(3))
               if mb:
                  if mb.group(1) and mb.group(2) and mb.group(3):
                     ret += processa_fragment(mb.group(1), escena, to_veu, " ")
                     ret += processa_fragment(mb.group(2), escena, Narrador, " ")
                     ret += processa_fragment(mb.group(3), escena, to_veu, "\n")
                  elif mb.group(1) and mb.group(2):
                     ret += processa_fragment(mb.group(1), escena, to_veu, " ")
                     ret += processa_fragment(mb.group(2), escena, Narrador, "\n")
                  elif mb.group(2) and mb.group(3):
                     ret += processa_fragment(mb.group(2), escena, Narrador, " ")
                     ret += processa_fragment(mb.group(3), escena, to_veu, "\n")
               else:
                  ret += processa_fragment(ma.group(3), escena, to_veu, "\n")
            else:
               ret += processa_fragment(sentencia, escena, Narrador, "\n")

            if stop or (estat=="anterior" and i>0) or (estat=="seguent" and i<n_escenes):
               f.close()
               break  # Detenir la lectura
            while en_pausa:
               time.sleep(0.1)  # Esperar mentre estigui en pausa

            print(ret, end="")
            posa_audio = True if audio_pendent else False
            retard = len(ret)/12 if posa_audio else 0.5
            socketio.emit('new_line', {'frase':ret, 'estat':estat, 'audio':posa_audio})  # Enviar el text al client
            time.sleep(retard)

   def principal():
      global actor, base_arxiu_text, estat
      #print("actor:", actor)
      if actor == "sencer":
         processa_escena("")
      else:
         escenes = glob.glob(f"{dir_dades}/{base_arxiu_text}-{actor}-*")
         if not escenes:
            processa_escena(actor)
         else:
            escenes.sort()
            n_escenes = len(escenes)
            i = 0
            while i < n_escenes:
               if stop:
                  break
               else:
                  if estat == "anterior" and i > 0:
                     i -= 1
                     estat = "inici"
                  elif estat == "seguent" and i < n_escenes:
                     i += 1
                     estat = "inici"
                  processa_escena(escenes[i], i, n_escenes)
                  i += 1

      socketio.emit('new_line', {'frase': 'Finalitzat', 'estat': "stop"})
      print('---------------- finalitzat ---------------------')

   # Esdeveniment que es dispara quan un client es connecta
   @socketio.on('connect')
   def handle_connect():
       print(f"{CB_YLW}Client connectat{C_NONE}")

   # Iniciamos la lectura del archivo en un hilo separado para no bloquear el servidor
   @socketio.on('inici')
   def handle_start():
       global fil, estat, stop, en_pausa
       print(f"{CB_YLW}botó inici{C_NONE}")
       estat = "inici"
       stop = False
       en_pausa = False
       if not fil or not fil.is_alive():
          fil = threading.Thread(target=principal)
          fil.start()

   @socketio.on('pausa')
   def handle_pause():
       global estat, en_pausa
       print(f"{CB_YLW}botó pausa{C_NONE}")
       estat = "pausa"
       en_pausa = not en_pausa

   @socketio.on('gravacio')
   def handle_gravacio():
       global estat, en_grabacio
       print(f"{CB_YLW}botó gravacio{C_NONE}")
       estat = "gravacio"
       en_grabacio = True

   @socketio.on('stop')
   def handle_stop():
       global estat, stop
       print(f"{CB_YLW}botó stop{C_NONE}")
       estat = "stop"
       stop = True  # Aturar la lectura de l'arxiu

   @socketio.on('anterior')
   def handle_anterior():
       global estat
       print(f"{CB_YLW}botó anterior{C_NONE}")
       estat = "anterior"

   @socketio.on('seguent')
   def handle_seguent():
       global estat
       print(f"{CB_YLW}botó seguent{C_NONE}")
       estat = "seguent"

   return app

if __name__ == "__main__":
   '''
   Permet la creació de l'aplicació a GitHub
   '''
   app = crear_app()
   '''
   Inicia los servicios flask en la terminal, lo cual, activa el acceso web
   equivale a ejecutar en una terminal el comando: flask run
   así, se activa el reconocimento de las aplicaciones Python en el puerto 5000 de localhost
   '''
   app.run(host='localhost', port=5000, debug=False)

