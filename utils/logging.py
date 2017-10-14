import logging
import functools

logger = logging.getLogger('execution')


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pass


def log_class(cls):
    class LoggerCls(object):
        def __init__(self, *args, **kwargs):
            self.wrapped = cls(*args, **kwargs)
            self.logger = logging.getLogger('{0}:{1}'.format(cls.__module__, cls.__name__))

        def __getattr__(self, name):
            attr = getattr(self.wrapped, name)
            if not callable(attr):
                return attr

            @functools.wraps(attr)
            def logging_wrapper(*args, **kwargs):
                self.logger.debug('ENTRY:{0}'.format(attr.__name__))
                try:
                    return attr(*args, **kwargs)
                except:
                    self.logger.exception('{0}'.format(attr.__name__), exc_info=True)
                    raise
                self.logger.debug('EXIT:{0}'.format(attr.__name__))

            return logging_wrapper

    return LoggerCls
