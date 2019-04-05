#!/usr/bin/env python
# -*- coding: utf-8 -*-
from LDAP2mail import LDAP2mail



with LDAP2mail('usuario', 'pass') as servidor_correo:
    servidor_correo
        .nuevo_correo('usuario@nlhp.cl', asunto='Otro asunto')
        .remitente('remitente_no_por_defecto@nlhpc.cl')
        .archivo_mensaje('path_al_archivo')
        .archivo_adjunto('path_al_archivo_adjunto')
        .envia()

    for usuario in datos_usuarios:
        servidor_correo.envia_correo()

