import os
import abc
import logging
from logging.handlers import SMTPHandler


class Config(metaclass=abc.ABCMeta):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'be1e74ae-a040-48e9-84bf-42d5e96e6363-dd1b82a0-43ca-40ff-96c3-1535eecd0fc5'
    SSL_DISABLE = True
    MAIL_SERVER = 'smtp.sendgrid.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sendgrid_username'
    MAIL_PASSWORD = 'sendgrid_password'
    MAIL_SUBJECT_PREFIX = '[boulderpython.org]'
    MAIL_SENDER = 'admin@boulderpython.org'

    SITE_ADMIN = os.environ.get('SITE_ADMIN') or 'recipient@site.com'
    CACHE_TYPE = os.environ.get('CACHE_TYPE') or 'gaememcached'
    GOOGLE_ANALYTICS_ID = 'UA-123456-78'

    @classmethod
    @abc.abstractmethod
    def init_app(cls, app):
        pass


class AppConfig(Config):
    """
    production config
    """
    @classmethod
    def init_app(cls, app, config=None):
        """
        config
        """
        # email errors to the administrators
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.SITE_ADMIN],
            subject=cls.MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        if config is not None:
            cls.__dict__


config = {
    'production': AppConfig,
    'testing': AppConfig,
    'default': AppConfig
}
