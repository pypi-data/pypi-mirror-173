

def test_import():
    from lgg import get_logger
    get_logger()


def test_logging():
    from lgg import logger

    logger.info('This is an info message')
    logger.debug('Debugging message')
    logger.error('Error message')
    logger.warning('File not found! An empty one is created')
