import logging
import inspect
import os
from datetime import datetime
from os import getenv


class Log:

    def __init__(self, file_log="APP_LOG"):
        self.__caller__ = inspect.currentframe().f_back.f_code

        self.__log_directory__ = getenv(file_log)
        if not os.path.exists(self.__log_directory__):
            os.makedirs(self.__log_directory__)

        self.__logger__ = None
        self.__configure_file_handler__()

    def info(self, msg):
        """ Log a message with severity 'INFO' on the root logger.  """

        if self.__date__ != datetime.today().date():
            self.__configure_file_handler__()

        return self.__logger__.info("INFO: "+str(msg))

    def warning(self, msg):
        """ Log a message with severity 'WARNING' on the root logger. """
        func = inspect.currentframe().f_back.f_code

        if self.__date__ != datetime.today().date():
            self.__configure_file_handler__()

        return self.__logger__.warning("WARN: %s on %s in %s: %i" % (
            str(msg),
            func.co_name,
            func.co_filename,
            func.co_firstlineno
        ))

    def warn(self, msg):
        """ Log a message with severity 'WARNING' on the root logger. """
        func = inspect.currentframe().f_back.f_code

        if self.__date__ != datetime.today().date():
            self.__configure_file_handler__()

        return self.__logger__.warning("WARN: %s on %s in %s: %i" % (
            str(msg),
            func.co_name,
            func.co_filename,
            func.co_firstlineno
        ))

    def error(self, msg):
        """ Log a message with severity 'ERROR' on the root logger. """
        func = inspect.currentframe().f_back.f_code

        if self.__date__ != datetime.today().date():
            self.__configure_file_handler__()

        return self.__logger__.error("ERRR: %s on %s in %s: %i" % (
            str(msg),
            func.co_name,
            func.co_filename,
            func.co_firstlineno
        ))

    def critical(self, msg):
        """ Log a message with severity 'CRITICAL' on the root logger. """
        func = inspect.currentframe().f_back.f_code

        if self.__date__ != datetime.today().date():
            self.__configure_file_handler__()

        return self.__logger__.critical("CRIT: %s on %s in %s: %i" % (
            str(msg),
            func.co_name,
            func.co_filename,
            func.co_firstlineno
        ))

    def __configure_file_handler__(self):
        self.__date__ = datetime.today().date()

        file_output = self.__log_directory__ + self.__date__.strftime("%Y%m%d") + '.log'
        msg_format = logging.Formatter('%(asctime)s %(message)s')

        self.__file_handler__ = logging.FileHandler(file_output)
        self.__file_handler__.setFormatter(msg_format)

        self.__logger__ = logging.getLogger(self.__caller__.co_filename)
        self.__logger__.handlers = []

        self.__logger__.setLevel(logging.DEBUG)
        self.__logger__.addHandler(self.__file_handler__)
