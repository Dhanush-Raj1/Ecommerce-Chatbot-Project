import sys
from src.utils.logger import logging


def error_message_detail(error, error_detail: sys):
    _, _, exc_tb_obj = error_detail.exc_info()       # (type, value, traceback),  exc_tb_obj - exception traceback object(3rd value)
     
    file_name = exc_tb_obj.tb_frame.f_code.co_filename       # tb_frame - frame information of trace back object
                                                             # f_code - code information such as line number, byte code of frame object(tb_frame)
                                                             # co_filename - file name of code object (f_code)
                                                             
    error_message = "Error occured in python script [{0}] line number [{1}] error message [{2}]".format( 
                                                                        file_name, exc_tb_obj.tb_lineno, str(error)  )
    
    return error_message    



class Custom_exception(Exception):                           # Customer_Exception class inherits from the built-in 'Exception' class
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
        
    
    def __str__(self):                        # representation method string 
        return self.error_message
    


# try:
#     print(hello)

# except Exception as e:
#     raise Custom_Exception(e, sys)
