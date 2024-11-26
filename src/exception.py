import sys
from src.logger import logging

class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        _, _, exc_tb = error_details.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        self.error_message = (
            f"Error occurred in python script name [{file_name}] "
            f"line number [{line_number}] error message [{error_message}]"
        )
        super().__init__(self.error_message)

    def __str__(self):
        return self.error_message


if __name__ == "__main__":
    try:
        a = 1 / 0
    except Exception as e:
        logging.info('An error occurred: dividing by zero.')
        raise CustomException(str(e), sys)
