from util import logger
import os, pytest


@pytest.fixture(scope='function')
def auto_log():
    test_name = os.environ.get('PYTEST_CURRENT_TEST').split(' ')[0]
    logger.info(f"##########start {test_name}##########")
    yield
    logger.info(f"##########Finish {test_name}##########")
