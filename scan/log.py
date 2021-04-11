import logging


def create_log_error(exception):
    logger = logging.getLogger(__name__)
    logger.error(str(exception))
