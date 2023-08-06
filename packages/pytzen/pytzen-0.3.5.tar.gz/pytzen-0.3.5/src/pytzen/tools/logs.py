from dataclasses import dataclass
import sys
import logging


@dataclass
class Logger:
    '''Builds solutions for logging methods and levels.
    '''

    def set_logger(self, level):
        '''Sets the logger environment for projects as a whole.
        '''
    
        global logger
        logger = logging.getLogger('pytzen')
        set_level = logging._nameToLevel[level]
        logger.setLevel(set_level)
        ch = logging.StreamHandler(sys.stdout)
        if level != 'DEBUG':
            msg = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        else:
            msg = '%(asctime)s\n%(message)s\n'
        formatter = logging.Formatter(msg)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False