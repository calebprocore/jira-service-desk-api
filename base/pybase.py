import os
import sys
import time as t
import inspect
import platform
from datetime import datetime as dt
from datetime import date
from pathlib2 import WindowsPath
from pathlib2 import PosixPath
from dotenv import load_dotenv
import base.exception as e


class PyBase(object):
    """
    """

    def __init__(self):
        """
        """
        error_msg = None
        self.this_class = __class__.__name__
        self.env = None
        self.start_time = None
        self.end_time = None
        self.system = platform.system()  # Windows, Mac, Linux
        self.app_home = os.getcwd()
        self.debug = False
        self.trace = True
        self.test_mode = False
        self.verbose = False
        self.print_stack_trace = True
        self.home = os.getcwd()
        # If True, will exit program if FatalException is raised, unless changed per call to
        # handle_exception()
        self.exit_on_fail = True

    def init(self):
        """
        Add any base initialization for entire app
        """
        success = False
        error_msg = None
        try:
            self.set_env()
        except Exception as e_init:
            success = False
            error_msg = 'Exception in pybase.init()'
            exit_on_fail = True
            self.handle_exception(exit_on_fail, error_msg, e_init)
        finally:
            return success

    def set_env(self):
        load_dotenv()
        self.env = os.getenv("ENV")
        if self.env is None:
            self.env = 'dev'
        # todo: assert env is not none, otherwise exit
        # print("ENV=" + self.env)

    def get_path(self, path):
        """
        Get passed in path object based on OS
        """
        if self.system == 'Windows':
            new_path = WindowsPath(path)
        else:
            new_path = PosixPath(path)
        return new_path

    def get_full_path(self, path):
        """
        Get full path by prepending self.app_home
        """
        full_path = None
        path = self.get_path(path)
        full_path = self.app_home / path
        return full_path

    def begin(self, method):
        if self.debug:
            print('\nBEGIN: ' + self.this_class + ' | '
                  + self.this_class, '==>', method + '()')

    def ping(self):
        self.begin(str(dt.utcnow()) + ' - ' + self.this_class + '.' + inspect.stack()[0][3])

    def get_date_utc(self):
        """
        Return a datetime of now
        """
        now = dt.utcnow()
        # print('now:', now)
        return now

    def print_date_time(self):
        # datetime object containing current date and time
        now = dt.now()

        print("now =", now)

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)

    def get_date_utc_str(self):
        """
        Return a datetime in string format
        """
        now = dt.utcnow()
        # print('now:', now)
        return str(now)

    def handle_exception(self, exit_on_fail, error_msg=None, ex=None):
        """
            Common error handler that can be called in every try/except
        """
        # self.print_error(error_msg, ex)
        if exit_on_fail:
            raise e.FatalException(ex, error_msg)
        else:
            raise e.Error(ex, error_msg)

    def print_error(self, error_msg=None, ex=None):
        """
        used for debug
            Can call directly, or through:
                =>   self.handle_error(error_msg, ex)
        """
        # print('PyBase.print_exception()')
        # self.begin(inspect.stack()[0][3])
        if error_msg is not None:
            print('ERROR:', error_msg)

        if ex is not None:
            print('\n---\nException in Class ==>', self.this_class, ex)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('Exception in Class ==>', self.this_class, exc_type, fname, '\n\tLine:',
                  exc_tb.tb_lineno)

    def print_runtime_env(self):
        # self.begin(inspect.stack()[0][3])
        print('\n--- [pybase.py] ---')
        print('OS:', self.system)
        print('OS Version:', platform.version())
        print('Python version:', platform.python_version())
        print('machine:', platform.machine())
        print('node:', platform.node())
        print('processor:', platform.processor())

        # print('\npython version:', platform.python_version())
        # print('python branch:', platform.python_branch())
        # print('python build:', platform.python_build())
        # print('python revision:', platform.python_revision())
        # print('python version tuple:', platform.python_version_tuple())
        # print('python implementation:', platform.python_implementation())
        # print('python compiler:', platform.python_compiler())

        print('debug:', self.debug)
        print('trace:', self.trace)
        print('test_mode:', self.test_mode)
        print('verbose:', self.verbose)
        print('print_stack_trace:', self.print_stack_trace)
        print('sys.path:', sys.path)

        print('---')
        print('self.env => ' + self.env)
        print('self.system => ' + self.system)
        print('self.app_home => ' + self.app_home)

    def log_start(self):
        self.start_time = self.get_date_utc()

    def log_end(self):
        self.end_time = self.get_date_utc()

    def print_runtime_stats(self):
        """
        Can be called at the end of a program to print runtime info

        """
        # datetime.combine(date.today(), exit) - datetime.combine(date.today(), enter)

        print('\n---------------------------------')
        print(self.this_class)
        print("Start:", str(self.start_time))
        print("End:  ", str(self.end_time))

        duration = self.end_time - self.start_time
        # datetime.combine(date.today(), exit) - datetime.combine(date.today(), enter)
        print("Duration:", duration)
        print('---------------------------------')
