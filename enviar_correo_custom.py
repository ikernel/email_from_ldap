#!/usr/bin/env python
# -*- coding: utf-8 -*-
from LDAP2mail import LDAP2mail
from getpass import getpass


## Estos usuarios ya enviaron la carta de recomendación.
## No es necesario enviárselas de nuevo.
__USUARIOS_OMITIDOS__ = [
    'daniel.aravena.p@usach.cl',      # Daniel Aravena
    'jos@ing.puc.cl',                 # Juan de Dios Ortúzar
    'maria.belen.camarada@gmail.com', # María Belén Camarada
    'worellana@unab.cl',              # Walter Orellana
    'eariel99@gmail.com',             # Eduardo Menendez
    'analilian.montero@gmail.com',    # Ana Montero
    'mauricio.flores@ug.uchile.cl',   # Mauricio Flores
    'marcos.casanova@ug.uchile.cl',   # Marcos Casanova
    'diego.velasco@cimav.edu.mx',     # Diego Velasco
    'julio.marin@meteo.uv.cl',        # Julio Marin Aguado
    'jab@meteo.uv.cl',                # Jorge Arévalo Bórquez
    'prodrigu@ubiobio.cl',            # Pedro Rodriguez
    'marioriquelme@ing.uchile.cl',    # Mario Riquelme
    'mauriciocerda@med.uchile.cl'     # Mauricio Cerda
]

## Es bueno enviar una copia a personas importantes.
## Para que se enteren y presionen sobre el resto de los usuarios.
__USUARIOS_ADICIONALES__ = [
    'jsanmart@dim.uchile.cl',         # Jaime San Martin
    'esvera@dim.uchile.cl',           # Eduardo Vera
    'amaass@dim.uchile.cl',           # Alejandro Vera
    'gguerrero@nlhpc.cl'              # Ginés
]

password = getpass()
with LDAP2mail('ppaillacar', password) as servidor:
    __ASUNTO__ = 'NLHPC - Apoyo Postulacion Fondequip'
    __REMITENTE__ = 'soporte@nlhpc.cl'

    nuevo_correo = servidor.\
        nuevo_correo_a_todos_en_ldap(__ASUNTO__).\
        mensaje_html('mensaje_repeticion_carta.html').\
        archivo_adjunto('carta_apoyo_NLHPC.pdf')

    for omitido in __USUARIOS_OMITIDOS__:
        print('Se omite el correo: ' + omitido)
        nuevo_correo = nuevo_correo.quitar_destinatario(omitido)

    for adicional in __USUARIOS_ADICIONALES__:
        print('Se adiciona el correo: ' + adicional)
        nuevo_correo = nuevo_correo.agregar_destinatario(adicional)

    nuevo_correo.envia()
