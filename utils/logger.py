import logging
import logging.handlers
from logging import critical, error, warning, info, debug
import time

from .singleton import Singleton

SYSLOG_ADDR = ('localhost', logging.handlers.SYSLOG_UDP_PORT)

LEVEL_DICT = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'notset': logging.NOTSET
    }

class Logger(object, metaclass=Singleton):
    """description of class"""

    def __init__(self, **kwargs):
        """
        Initialise a Logger class. This is a singleton so it instanciate
        only once.
        A default formatter is set for every handlers.
        A level of debug is determined by: 'critical', 'error',
        'warning', 'info', 'debug', 'notset' from the most import to the least
        """
        self.level = kwargs.get('level', 'debug')
        self.handlers = list()
        self.format = logging.Formatter(
            '[%(asctime)s][%(levelname)s] %(message)s')
        self.format.default_time_format = '%H:%M:%S'
        self.format.default_msec_format = '%s.%03d'
        self.__set = False
        return super().__init__(**kwargs)

    def __add_handler_to_basicconfig(self, handler, new_level) -> None:
        """
        Add the handler to the list of active ones and call basicConfig()
        Assertion is made when the handler is already in the list or
        the new level set does not exist
        """
        assert new_level in LEVEL_DICT.keys() and handler not in self.handlers
        self.handlers.append(handler)
        logging.basicConfig(handlers=self.handlers, level=LEVEL_DICT[new_level])

    def _handler_factory(self, handlertype, *args, **kwargs) -> logging.Handler:
        handler = handlertype(*args)
        handler.setLevel(LEVEL_DICT[kwargs.get('level', 'notset')])
        handler.setFormatter(self.format)
        return handler

    def set_config(self) -> None:
        """
        Run the basic config command using the handlers previously defined
        This command should be used only once
        """
        assert self.level in LEVEL_DICT.keys() and not self.__set
        logging.basicConfig(handlers=self.handlers, level=LEVEL_DICT[self.level])
        self.__set = True

    def add_file_handler(self,  destfolder: str = "./logs/",
                         nameformat: str = "%y%m%d_%H%M%S", **kwargs) -> None:
        """
        Give a file nameformat and a folder to write logs in a file
        The nameformat goes through time.strftime()
        kwargs:
            level: set the logging level of this specific handler
        """
        self.handlers.append(self._handler_factory(
            logging.FileHandler,
            "{}/{}.log".format(destfolder, time.strftime(nameformat)),
            **kwargs))

    def add_stream_handler(self, stream, **kwargs) -> None:
        """
        Add a stream to output the logs
        kwargs:
            level: set the logging level of this specific handler
        """
        self.handlers.append(self._handler_factory(
            logging.StreamHandler,
            stream,
            **kwargs))

    def add_udp_handler(self, host, port, **kwargs) -> None:
        """
        Add a UDP handler (not really usefull)
        kwargs:
            level: set the logging level of this specific handler
        """
        self.handlers.append(self._handler_factory(
            logging.handlers.DatagramHandler,
            host, port,
            **kwargs))

    def add_syslog_handler(self, address=SYSLOG_ADDR, **kwargs) -> None:
        """
        Add a SysLogHandler to the log output
        The basic UDP socket is used for the communication
        args:
            address: a tuple representing (host, port) or a string '/dev/log'
        kwargs:
            level: set the logging level of this specific handler
        """
        self.handlers.append(self._handler_factory(
            logging.handlers.SysLogHandler,
            address=address, **kwargs))
