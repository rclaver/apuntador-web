#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 16:32:05 2025
@author: rafael

Las aplicaciones Python con Flask deben ejecutarse desde una terminal.
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.

Ejecutar en la nube:
- subir el repositorio a Github
- crear una aplicación en dashboard.render.com
"""
import os
from flask import Flask, render_template, request
#from dotenv import load_dotenv

def crear_app():
   app = Flask(__name__) #instancia de Flask
   key_secret = os.getenv("API_KEY")

   @app.route("/index", methods = ["GET", "POST"])
   def index():
      info = ""
      if request.method == "POST":
         info = request.form.get("enviar")
      return render_template("index.tpl")


   @app.route("/apuntador", methods = ["GET", "POST"])
   def apuntador():
      html = render_template("apuntador.tpl", actor="joan")
      return html

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
   app.run()
