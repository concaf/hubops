import logging

def log_info(message):
    logging.basicConfig(filename='logs_info',level=logging.INFO)
    logging.info(message)

def log_error(message):
    logging.basicConfig(filename='logs_error',level=logging.ERROR)
    logging.error(message)