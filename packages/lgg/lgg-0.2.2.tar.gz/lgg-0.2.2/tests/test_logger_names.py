def test_anonymous():
    from lgg import logger
    assert logger.name == 'nameless'


def test_different_names():
    from lgg import get_logger
    print()
    l = list(range(1, 4))
    loggers = [get_logger(f'logger{i}') for i in l]

    for i, logger in zip(l, loggers):
        assert logger.name == f'logger{i}'
        logger.info(f'Hello from logger {i}')


def test_same_names():
    from lgg import get_logger
    loggers = [get_logger('logger_name') for _ in range(2)]

    for logger in loggers:
        logger.info('Hello!')
        logger.error('Bye!')
