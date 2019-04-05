# -*- coding: utf-8 -*-
import smtplib
import mimetypes
from copy import deepcopy
from os.path import isfile
from LDAPController import LDAPController
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email import encoders


_SERVIDOR_CORREO = 'zimbra.nlhpc.cl'
_CODIFICACION = 'utf-8'


class NoHayDestinatarios(Exception):
    """Excepción que indica que no existen destinatarios en la lista de correo"""
    def __init__(self, mensaje):
        self._mensaje = mensaje

    def __str__(self):
        return self._mensaje


class NoHayMensaje(Exception):
    """Excepción que indica que el mensaje a enviar está vacío"""
    def __init__(self, mensaje):
        self._mensaje = mensaje

    def __str__(self):
        return self._mensaje


class LDAP2mail:
    def __init__(self, usuario, password):
        self.__nombre_usuario = usuario
        self.__password = password

        self._destinatarios = []
        self._asunto = '[NLHPC] Comunicado'     ## Asunto por defecto
        self._remitente = 'soporte@nlhpc.cl'    ## Remitente por defecto
        self._mensaje = None

    def __enter__(self):
        self.conexion = smtplib.SMTP_SSL(_SERVIDOR_CORREO)
        self._comprobar_credenciales()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.conexion = None
        del self.conexion

    def _comprobar_credenciales(self):
        """Comprobación de las credenciales SMTP del correo"""
        try:
            self.conexion.login(self.__nombre_usuario, self.__password)
        except smtplib.SMTPAuthenticationError:
            print('Nombre de usuario o contraseña incorrecta')
            raise

    def nuevo_correo(self, asunto=None):
        """Inicio de configuración para el envío de un correo"""
        self._mensaje = MIMEMultipart()
        if asunto is not None:
            self._asunto = asunto

        return self

    def nuevo_correo_a_todos_en_ldap(self, asunto=None):
        """
        Inicio de la configuración para el envío de un correo a todos los
        usuarios que se encuentren actualmente en LDAP
        """
        with LDAPController() as qldap:
            for datos_usuario in qldap.filtra(['correo']):
                self._destinatarios.append(datos_usuario['correo'])

        self._mensaje = MIMEMultipart()
        if asunto is not None:
            self._asunto = asunto

        return self

    def nuevo_correo_a_todos_test(self, asunto=None):
        """Envía un mensaje a todos quienes existan en la lista de test"""
        correos_test = [
            'ppaillacar@nlhpc.cl',
            'pipo88@gmail.com',
            'paulo.paillacar@outlook.com'
        ]
        for correo_test in correos_test:
            self._destinatarios.append(correo_test)

        self._mensaje = MIMEMultipart()
        if asunto is not None:
            self._asunto = asunto

        return self

    def agregar_destinatario(self, correo):
        """Agrega un nuevo destinatario a la carátula del correo"""
        self._destinatarios.append(correo)
        return self

    def quitar_destinatario(self, correo):
        """Quita un destinatario de la lista de correos"""
        try:
            self._destinatarios.remove(correo)
        except ValueError:
            print('No existe el destinatario: ' + correo)

        return self

    def remitente(self, remitente):
        """Cambia el remitente del correo"""
        self._remitente = remitente
        return self

    def mensaje(self, mensaje_string):
        """Considera el mensaje a enviar desde un string Python"""
        cuerpo_mensaje = MIMEText(mensaje_string.decode(_CODIFICACION), 'plain', _CODIFICACION)
        self._mensaje.attach(cuerpo_mensaje)
        return self

    def mensaje_html(self, ruta_html):
        """Parsea un HTML para ser incluído como mensaje"""
        handler_archivo = open(ruta_html, 'rb')
        cuerpo_mensaje = MIMEText(handler_archivo.read().decode(_CODIFICACION), 'html', _CODIFICACION)
        self._mensaje.attach(cuerpo_mensaje)
        return self

    def archivo_adjunto(self, ruta_archivo):
        """Adjunta un archivo al mensaje que se enviará"""
        def es_correcto(archivo):
            if archivo is None:
                return False
            if isfile(archivo):
                return True

        if not es_correcto(ruta_archivo):
            return self

        archivo_handler = open(ruta_archivo, 'rb')
        ctype, codificacion = mimetypes.guess_type(ruta_archivo)
        if ctype is None or codificacion is not None:
            ctype = 'application/octet-stream'

        adjunto = None
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            adjunto = MIMEText(archivo_handler.read(), _subtype=subtype)
        else:
            adjunto = MIMEBase(maintype, subtype)
            adjunto.set_payload(archivo_handler.read())
            encoders.encode_base64(adjunto)

        adjunto.add_header('Content-Disposition', 'attachment', filename=ruta_archivo)
        self._mensaje.attach(adjunto)
        archivo_handler.close()
        return self

    def envia(self):
        """Envía un correo a todos los destinatarios registrados"""
        if len(self._destinatarios) == 0:
            raise NoHayDestinatarios('La lista de destinatarios está vacía')
        if self._remitente is None:
            raise NoHayMensaje('El mensaje del correo no puede estar vacío.\nEspecifique el cuerpo del mensaje')

        self._mensaje['From'] = self._remitente
        self._mensaje['Subject'] = self._asunto
        self._mensaje.preamble = self._asunto
        for destinatario in self._destinatarios:
            este_mensaje = deepcopy(self._mensaje)
            este_mensaje['To'] = destinatario
            self.conexion.sendmail(self._remitente, destinatario, este_mensaje.as_string())
            print('Correo enviado al destinatario: ' + destinatario)
