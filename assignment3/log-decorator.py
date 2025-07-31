
# one time setup
import logging
from functools import wraps 
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log","a"))
...
# To write a log record:
logger.log(logging.INFO, "this string would be logged")


def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs): 
        if args: 
            position_params = list(args) 
        else: 
            position_params = "none" 

        if kwargs: 
            keyword_params = dict(kwargs) 
        else: 
            keyword_params = "none"
        
        result = func(*args, **kwargs)

        log_message = (f"function:{func.__name__}"
                       f"positional parameters: {position_params}"
                       f"keyword parameters: {keyword_params}"
                       f"return: {result}")
        
        logger.log(logging.INFO, log_message)

        return result 
    return wrapper

#Task 3 
@logger_decorator
def hello(): 
    print("Hello, World!")

#Task 4 
@logger_decorator
def check_args(*args): 
    return True 

#Task 5 
@logger_decorator
def check_dec(**kwargs): 
    return logger_decorator 


hello()
check_args(46,42,23)
check_dec(name="June",day="19")
