import os
import sys
import logging
from typing import Optional
from datetime import datetime

class ColorFormatter(logging.Formatter):
    # ANSI Colour Codes
    COLORS = {
        'ERROR': '\033[31m',      # Red
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'CRITICAL': '\033[35m',   # Magenta
        'DIM': '\033[2m',         # Dim
        'BOLD': '\033[1m',        # Bold
        'RESET': '\033[0m',       # Reset
    }
    
    def format(self, record):
        # Create The Log Format With Specified Colours
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        bold = self.COLORS['BOLD']
        dim = self.COLORS['DIM']
        
        # Format Timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        # Create Formatted Messages
        log_message = (
            f"{dim}[ {timestamp} ]{reset} "
            f"{color}{bold}[ {record.levelname:^8} ]{reset} "
            f"{bold}{record.name}{reset} "
            f"→ {record.getMessage()}"
        )
        
        if record.exc_info:
            log_message += f"\n{self.formatException(record.exc_info)}"
            
        return log_message

class BeautifulLogger:    
    def __init__(self, name: str = "AppLogger", level: str = "INFO", 
                 log_to_file: bool = False, log_file: str = "../app.log"):
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))

        self.logger.handlers.clear()

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColorFormatter())
        self.logger.addHandler(console_handler)
        
        if log_to_file:
            os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else 'logs', exist_ok=True)
            if not os.path.dirname(log_file):
                log_file = os.path.join('logs', log_file)
                
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, *args, **kwargs):
        """Log Debug Message"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """Log Info Message"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log Warning Message"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log Error Message"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log Critical Message"""
        self.logger.critical(message, *args, **kwargs)
    
    def success(self, message: str, *args, **kwargs):
        """Log Success Message"""
        success_msg = f"{message}"
        self.logger.info(success_msg, *args, **kwargs)
    
    def failure(self, message: str, *args, **kwargs):
        """Log Failure Message"""
        failure_msg = f"{message}"
        self.logger.error(failure_msg, *args, **kwargs)
    
    def separator(self, char: str = "=", length: int = 50):
        """Log A Separator Line"""
        self.logger.info(char * length)
    
    def header(self, title: str, char: str = "="):
        separator_length = max(50, len(title) + 10)
        self.separator(char, separator_length)
        self.logger.info(f"{title:^{separator_length}}")
        self.separator(char, separator_length)

_default_logger = BeautifulLogger(name="VidBot", level="INFO")

def debug(message: str, *args, **kwargs):
    """Quick Debug Logging"""
    _default_logger.debug(message, *args, **kwargs)

def info(message: str, *args, **kwargs):
    """Quick Info Logging"""
    _default_logger.info(message, *args, **kwargs)

def warning(message: str, *args, **kwargs):
    """Quick Warning Logging"""
    _default_logger.warning(message, *args, **kwargs)

def error(message: str, *args, **kwargs):
    """Quick Error Logging"""
    _default_logger.error(message, *args, **kwargs)

def critical(message: str, *args, **kwargs):
    """Quick Critical Logging"""
    _default_logger.critical(message, *args, **kwargs)

def success(message: str, *args, **kwargs):
    """Quick Success Logging"""
    _default_logger.success(message, *args, **kwargs)

def failure(message: str, *args, **kwargs):
    """Quick Failure Logging"""
    _default_logger.failure(message, *args, **kwargs)

def separator(char: str = "=", length: int = 50):
    """Quick Separator Logging"""
    _default_logger.separator(char, length)

def header(title: str, char: str = "="):
    """Quick Header Logging"""
    _default_logger.header(title, char)

def get_logger(name: str = "VidBot", level: str = "INFO", 
               log_to_file: bool = False, log_file: str = "../app.log") -> BeautifulLogger:

    return BeautifulLogger(name, level, log_to_file, log_file)
