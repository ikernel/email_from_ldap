#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ejemplo de cómo utilizar la clase LDAPController para mostrar datos de usuarios desde LDAP
"""
from LDAPController import LDAPController
import random

with LDAPController() as qldap:
    with open('usuarios_omitidos.txt', 'rb') as handler_omitidos:
        with open('orden_top_usuarios.txt', 'rb') as handler_prioritarios:
            usuarios_omitidos = [omitido.strip() for omitido in handler_omitidos.readlines()]
            orden_usuarios = [prioritario.strip() for prioritario in handler_prioritarios.readlines()]

            def pre_filtra(fila):
                return fila['gecos'][0] not in usuarios_omitidos

            resultado = qldap.filtra(['nombre_completo', 'correo', 'institucion', 'area', 'situacion_academica', 'descripcion_proyecto', 'investigador_principal'], pre_filtro=pre_filtra)        # resultado = qldap.filtra(['nombre', 'correo'])

            usuarios_ordenados = []
            for usuario_prioritario in orden_usuarios:
                posicion_usuario = [i for i,x in enumerate(resultado) if x['nombre_completo'] == usuario_prioritario]
                usuarios_ordenados.append(resultado.pop(posicion_usuario[0]))

            random.shuffle(resultado, random.random)
            for res in resultado:
                usuarios_ordenados.append(res)

            print("<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"utf-8\">\n<title>Datos usuarios</title>\n</head><body>")
            for usuario in usuarios_ordenados:
                print('<b>Nombre: </b>' + usuario['nombre_completo'] + '<br />')
                print('<b>Situación académica: </b>' + usuario['situacion_academica'] + '<br />')
                print('<b>Correo electrónico: </b>' + usuario['correo'] + '<br />')
                print('<b>Institución: </b>' + usuario['institucion'] + '<br />')
                print('<b>Área: </b>' + usuario['area'] + '<br />')
                print('<b>Investigador principal: </b>' + usuario['investigador_principal'] + '<br />')
                print('<b>Descripción proyecto: </b>' + usuario['descripcion_proyecto'] + '<br />')
                print('<hr />')
            print("\n</body></html>")
