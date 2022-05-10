import os
import configparser
from base.pybase import PyBase


class Config(PyBase):

    def __init__(self):
        super().__init__()
        self.config_parser = None

    def init(self):
        """
            Read any/all config files needed by this app and set params for use throughout
        """
        super().init()
        success = False
        error_msg = None
        try:
            print('Config.init()')
            if self.config_parser is None:
                self.config_parser = configparser.ConfigParser()

            ini_file = self.env + '.ini'
            ini_file = os.path.join('config', ini_file)
            print('ini_file: ' + ini_file)
            self.read_ini(ini_file)

            # if self.debug:
            #     super().print_config_ini()    # prints contents of config parser
        except Exception as e_init:
            success = False
            error_msg = 'Exception in config.init()'
            exit_on_fail = True
            self.handle_exception(exit_on_fail, error_msg, e_init)
        finally:
            return success

    def get_value(self, section, key):
        return self.config_parser[section][key]

    def read_ini(self, ini_file):
        """
            Reads .ini file
            ini_file is just the file, relative to cwd, not full path
            todo: add, if file not found, throw fatal exception, exit
        """
        success = False
        error_msg = None
        try:
            self.config_parser.read(ini_file)
            success = True
        except Exception as e_init:
            success = False
            error_msg = 'Exception in config.init()'
            exit_on_fail = True
            self.handle_exception(exit_on_fail, error_msg, e_init)
        finally:
            return success
