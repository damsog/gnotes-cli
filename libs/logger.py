import logging
import colorful


# My logger configuration
class Logger:
    def __init__(self, LEVEL, COLORED=False, TAG_MODULE=None):
        # Logger Configuration
        self.COLORED = COLORED

        if TAG_MODULE is not None:
            self.TAG_MODULE = TAG_MODULE
        else: 
            self.TAG_MODULE = ''

        self.logger = logging.getLogger(__name__)
        self.logger_format = '%(message)s'
        self.logger_date_format = '[%Y/%m/%d %H:%M:%S %Z]'
        colorful.use_style('solarized')

        if LEVEL == "DEBUG":
            logging.basicConfig(level=logging.DEBUG, format=self.logger_format, datefmt=self.logger_date_format)
        else:
            logging.basicConfig(level=logging.INFO,  format=self.logger_format, datefmt=self.logger_date_format)
    
    def color(self, message, color="no"):

        colorize = {
            'yellow':colorful.yellow(message),
            'orange':colorful.orange(message),
            'red':colorful.red(message), 
            'magenta':colorful.magenta(message),
            'violet':colorful.violet(message), 
            'blue':colorful.blue(message),
            'cyan':colorful.cyan(message),
            'green':colorful.green(message),
            'no':message
        }

        return colorize.get(color, 'Not a valid color')

    def info(self, message, color="no"):
        if self.COLORED:
            self.logger.info( self.color(f'{self.TAG_MODULE} {message}', color) )
        else:
            self.logger.info(f'{self.TAG_MODULE}: {message}')
    
    def debug(self, message, color="no"):
        if self.COLORED:
            self.logger.debug( self.color(f'{self.TAG_MODULE}: {message}', color) )
        else:
            self.logger.debug(f'{self.TAG_MODULE}: {message}')

    def warning(self, message, color="no"):
        if self.COLORED:
            self.logger.warning( self.color(f'{self.TAG_MODULE}: {message}', color) )
        else:
            self.logger.warning(f'{self.TAG_MODULE}: {message}')
    
    def error(self, message, color="no"):
        if self.COLORED:
            self.logger.error( self.color(f'{self.TAG_MODULE}: {message}', color) )
        else:
            self.logger.error(f'{self.TAG_MODULE}: {message}')