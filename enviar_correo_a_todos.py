#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Envía un correo a todos los usuarios en LDAP.

Usage:
    send2all (-u USUARIO | --usuario=USUARIO) [-r REM | --remitente=REM] (-s SUB | --asunto=SUB) [-a ADJUNTO | --archivo=ADJUNTO] ARCHIVO_MENSAJE
    send2all -h | --ayuda | --version

Options:
    -h, --ayuda                     Muestra esta pantalla de ayuda.
    -r REM, --remitente=REM         Correo que se utilizará como remitente [default: soporte@nlhpc.cl].
    -s SUB, --asunto=SUB            Asunto del correo.
    -u USUARIO, --usuario=USUARIO   Nombre de usuario para enviar el correo (Ojo! puede no ser igual al remitente).
    -a ADJUNTO, --archivo=ADJUNTO   Ruta de un archivo que irá adjunto al correo.
    --version                       Versión de la aplicación.
"""
from LDAP2mail import LDAP2mail
from getpass import getpass
from docopt import docopt


if __name__ == '__main__':
    _IDENTIFICACION_NLHPC = '\n\nLaboratorio Nacional de Cómputo de Alto Rendimiento\nCentro de Modelamiento Matemático (CMM)\nFacultad de Ciencias Físicas y Matemáticas\nUniversidad de Chile'
    esta_version = 'Send to All 1.0' + _IDENTIFICACION_NLHPC
    parametros = docopt(__doc__, version=esta_version)

    if parametros['--version']:
        print(esta_version)
        exit(0)
    if parametros['--ayuda']:
        print(__doc__)
        exit(0)

    password = getpass()
    with LDAP2mail(parametros['--usuario'], password) as servidor:
        servidor.\
            nuevo_correo_a_todos_en_ldap(parametros['--asunto']).\
            agregar_destinatario('gguerrero@nlhpc.cl').\
            remitente(parametros['--remitente']).\
            mensaje_html(parametros['ARCHIVO_MENSAJE'])

	if parametros['--archivo']:
		for adjunto in parametros['--archivo'].split(':'):
		    servidor.archivo_adjunto(adjunto)

        servidor.envia()
