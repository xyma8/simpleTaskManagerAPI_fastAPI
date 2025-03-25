import logging
import sys


def setup_logger():
    # Create a logger
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a handler that outputs messages to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)  # Set the logging level for the handler

    # Format the logger messages
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)
    return logger
