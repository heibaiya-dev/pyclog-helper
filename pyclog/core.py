import inspect
from datetime import datetime
from typing import Optional, List, Any

from .config import LogConfig, LogMessage, LogLevel, DEFAULT_CONFIG
from .formatter import LogFormatter, SimpleFormatter
from .handler import FileHandler, RotatingFileHandler, ConsoleHandler


class Pyclog:
    def __init__(self, config: Optional[LogConfig] = None, 
                 formatter: Optional[LogFormatter] = None):
        self.config = config or DEFAULT_CONFIG
        self.formatter = formatter or SimpleFormatter()
        self.handlers: List[Any] = []
        self._lock = False
        
        self._Initialize_Handlers()

    def _Initialize_Handlers(self) -> None:
        file_handler = RotatingFileHandler(self.config, self.formatter)
        self.handlers.append(file_handler)

    def Add_Handler(self, handler: Any) -> None:
        self.handlers.append(handler)

    def Remove_Handler(self, handler: Any) -> bool:
        try:
            self.handlers.remove(handler)
            return True
        except ValueError:
            return False

    def Set_Formatter(self, formatter: LogFormatter) -> None:
        self.formatter = formatter
        for handler in self.handlers:
            if hasattr(handler, 'formatter'):
                handler.formatter = formatter

    def Set_Log_Level(self, level: LogLevel) -> None:
        self.config.min_log_level = level

    def Debug(self, message: str, **kwargs) -> bool:
        return self._Log(LogLevel.DEBUG, message, **kwargs)

    def Info(self, message: str, **kwargs) -> bool:
        return self._Log(LogLevel.INFO, message, **kwargs)

    def Warning(self, message: str, **kwargs) -> bool:
        return self._Log(LogLevel.WARNING, message, **kwargs)

    def Error(self, message: str, **kwargs) -> bool:
        return self._Log(LogLevel.ERROR, message, **kwargs)

    def Critical(self, message: str, **kwargs) -> bool:
        return self._Log(LogLevel.CRITICAL, message, **kwargs)

    def _Log(self, level: LogLevel, message: str, **kwargs) -> bool:
        if level.value < self.config.min_log_level.value:
            return False
        
        timestamp = self.formatter.Format_Timestamp()
        module_name = self._Get_Calling_Module_Name()
        
        log_message = LogMessage(
            level=level,
            message=message,
            module_name=module_name,
            timestamp=timestamp,
            extra_fields=kwargs
        )
        
        formatted_message = self.formatter.Format_Message(log_message)
        
        success = True
        for handler in self.handlers:
            if not handler.Write_Log(formatted_message):
                success = False
        
        return success

    def _Get_Calling_Module_Name(self) -> str:
        try:
            frame = inspect.currentframe()
            if frame is None:
                return "unknown"
            
            for _ in range(3):
                frame = frame.f_back
                if frame is None:
                    break
            
            if frame is not None:
                module = inspect.getmodule(frame)
                if module is not None and module.__name__ != '__main__':
                    return module.__name__
                
                filename = frame.f_code.co_filename
                if filename:
                    return filename.split('\\')[-1].split('/')[-1].replace('.py', '')
            
            return "unknown"
        except Exception:
            return "unknown"

    def Create_Log_File(self, file_path: str, 
                       max_size: Optional[int] = None,
                       backup_count: Optional[int] = None) -> bool:
        try:
            from copy import deepcopy
            
            new_config = deepcopy(self.config)
            new_config.log_file_path = file_path
            
            if max_size is not None:
                new_config.max_file_size = max_size
            if backup_count is not None:
                new_config.backup_count = backup_count
            
            new_handler = RotatingFileHandler(new_config, self.formatter)
            self.handlers.append(new_handler)
            return True
        except Exception as e:
            print(f"Error creating log file: {e}")
            return False

    def Add_Console_Output(self) -> None:
        console_handler = ConsoleHandler(self.formatter)
        self.handlers.append(console_handler)

    def Flush(self) -> None:
        for handler in self.handlers:
            handler.Flush()

    def Close(self) -> None:
        for handler in self.handlers:
            handler.Close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Close()
        return False


def Create_Logger(log_file_path: str = "app.log",
                  max_file_size: int = 10 * 1024 * 1024,
                  backup_count: int = 5,
                  enable_date_rotation: bool = False,
                  log_format: Optional[str] = None,
                  time_format: Optional[str] = None) -> Pyclog:
    config = LogConfig(
        log_file_path=log_file_path,
        max_file_size=max_file_size,
        backup_count=backup_count,
        enable_date_rotation=enable_date_rotation
    )
    
    formatter = None
    if log_format or time_format:
        formatter = LogFormatter(
            format_string=log_format or "[%(asctime)s] [%(levelname)s] %(message)s",
            time_format=time_format or "%Y-%m-%d %H:%M:%S"
        )
    
    return Pyclog(config, formatter)


def Get_Logger(name: str = "default") -> Pyclog:
    _loggers = {}
    
    if name not in _loggers:
        _loggers[name] = Pyclog()
    
    return _loggers[name]
