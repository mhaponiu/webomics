import logging
logger = logging.getLogger('cgb')  # logger z settings.py

from inspect import stack
import datetime

# Nazwa aktualnej funkcji: stack()[0][3]; [1][3] jeszcze poprzednia, czyli ta ktora wola LOG_...

def createMsg(function_name, msg):
    return str(function_name) + " ---\t" + str(msg)

def INFO(msg):
    function_name = stack()[1][3]
    logger.info(createMsg(function_name, msg));
    
def WARN(msg):
    function_name = stack()[1][3]
    logger.warning(createMsg(function_name, msg))
    
def DEBUG(msg):
    function_name = stack()[1][3]
    logger.debug(createMsg(function_name, msg))