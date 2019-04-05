# -*- coding: utf-8 -*-
import ldap
from ConfigParser import ConfigParser

class LDAPController:
    __DEFAULT_SEARCH_FILTER = '(objectClass=*)'

    def __init__(self, config_file_path=None):
        self.config_file = config_file_path if config_file_path is not None else 'etc/ldap-client.conf'

        config_handler = ConfigParser()
        config_handler.read(self.config_file)

        self.host_url = config_handler.get('conection_parameters', 'host_url')
        self.basedn = config_handler.get('conection_parameters', 'basedn')
        self.tabla_correspondencia = dict(config_handler.items('equivalence_table'))

    def __enter__(self):
        self.client = ldap.initialize(self.host_url)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """En realidad nada pasa aquí"""
        pass
        
    def filtra(self, terminos_filtro, pre_filtro=None):
        """Realiza una consulta al LDAP filtrando por los términos que se le indiquen"""
        for termino in terminos_filtro:
            # Revisar que todos los términos de filtro existan (o estén bien escritos)
            if termino not in list(self.tabla_correspondencia.iterkeys()):
                raise NameError('No se reconoce el término \'' + termino + '\'')

        # Aceptar todos los datos por defecto
        if pre_filtro is None:
            pre_filtro = lambda res: True

        terminos_busqueda = [self.tabla_correspondencia[filtro] for filtro in terminos_filtro]
        resultados = self.client.search_s(self.basedn, ldap.SCOPE_SUBTREE, self.__DEFAULT_SEARCH_FILTER, terminos_busqueda)

        def comprueba(fila):
            # Comprueba que todas las filas, de los terminos especificados, tengan resultados
            terminos_fila = list(fila.iterkeys())
            existen_resultados_por_termino = [termino in terminos_fila for termino in terminos_busqueda]
            return all(existen_resultados_por_termino)

        def empaca(fila):
            # Retorna los resultados en un diccionario, aprovechando de formatear la salida
            return {
                filtro: fila[self.tabla_correspondencia[filtro]][0].strip()
                for filtro in terminos_filtro
            }

        return [empaca(resultado) for dn, resultado in resultados if comprueba(resultado) and pre_filtro(resultado)]


def extraer(por_terminos):
    with LDAPController() as qldap:
        return qldap.filtra(por_terminos)
