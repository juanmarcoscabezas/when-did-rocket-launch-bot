import functools
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    filename='./logs/logs.txt',
    format=' %(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

def telegram_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start_time = time.time()
            res =  func(*args, **kwargs)
            end_time = time.time()
            logger.info(f'Execution time for {func.__name__}: {end_time - start_time}')
            return res
        except Exception as e:
            logger.exception(f'Exception raised in {func.__name__}. Exceotion: {str(e)}')
    return wrapper

def db_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start_time = time.time()
            res =  func(*args, **kwargs)
            chat_id = None
            if kwargs.get('data'):
                chat_id = kwargs.get('data')['chat_id']
            elif kwargs.get('chat_id'):
                chat_id = kwargs.get('chat_id')
                
            end_time = time.time()
            logger.info(f'Execution time for {func.__name__}: {end_time - start_time}. chat_id: {chat_id}')
            return res
        except Exception as e:
            logger.exception(f'Exception raised in {func.__name__}. Exceotion: {str(e)}')
    return wrapper