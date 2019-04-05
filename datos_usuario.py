#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Datos de usuarios desde LDAP

Filtra columnas desde todos los datos en LDAP según los términos suministrados.
Los filtros disponibles pueden ser consultados mediante la opción '-l' o '--lista-terminos'.
Por defecto son utilizados los términos previamente mapeados que se encuentren en la siguiente
ruta: 'etc/ldap-client.conf'. Es buena idea contar con un archivo previamente generado. Se puede
utilizar uno distinto al por defecto pasando como parámetro la ruta al parámetro '--conf'.

Usage:
    datas_usuario.py [-hl] | <terminos>...

Options:
    -h, --help                               Muestra esta ayuda
    -l, --lista-terminos                     Lista los terminos disponibles para filtrar

"""
from docopt import docopt
from LDAPController import extraer
from ConfigParser import ConfigParser

if __name__ == '__main__':
    args = docopt(__doc__, version="Datos de Usuario 1.1")

    if args['--lista-terminos']:
        config_handler = ConfigParser()
        config_handler.read('etc/ldap-client.conf')

        for termino, simil_ldap in config_handler.items('equivalence_table'):
            print('{0} -> {1}'.format(simil_ldap, termino))
        exit()

    for data in extraer(args['<terminos>']):
        print(', '.join([data[termino] for termino in args['<terminos>']]))
