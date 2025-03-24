# logging_config.py
import logging

def setup_logging(log_file='app.log'):
    """
    Setup logging configuration to log to a single file.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create file handler to save logs to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)
    
    return logger
