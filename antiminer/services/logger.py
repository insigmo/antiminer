import logging
import sys

def setup_logger():
    logger = logging.getLogger("antiminer")
    logger.setLevel(logging.DEBUG)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[AntiMiner][%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


