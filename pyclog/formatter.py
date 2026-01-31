from datetime import datetime
from typing import Dict, Any
import re

from .config import LogMessage, LogLevel


class LogFormatter:
    def __init__(self, format_string: str = "[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s", 
                 time_format: str = "%Y-%m-%d %H:%M:%S"):
        self.format_string = format_string
        self.time_format = time_format
        self._pattern = re.compile(r"%\((\w+)\)s")

    def Format_Message(self, message: LogMessage) -> str:
        format_dict = self._Build_Format_Dict(message)
        formatted_message = self.format_string
        
        for key, value in format_dict.items():
            placeholder = f"%({key})s"
            formatted_message = formatted_message.replace(placeholder, str(value))
        
        return formatted_message

    def _Build_Format_Dict(self, message: LogMessage) -> Dict[str, Any]:
        format_dict = {
            "asctime": message.timestamp,
            "levelname": message.level.name,
            "levelno": message.level.value,
            "module": message.module_name,
            "message": message.message,
        }
        
        for key, value in message.extra_fields.items():
            format_dict[key] = value
        
        return format_dict

    def Format_Timestamp(self, timestamp: datetime = None) -> str:
        if timestamp is None:
            timestamp = datetime.now()
        return timestamp.strftime(self.time_format)

    def Set_Format(self, format_string: str) -> None:
        self.format_string = format_string

    def Set_Time_Format(self, time_format: str) -> None:
        self.time_format = time_format


class SimpleFormatter(LogFormatter):
    def __init__(self):
        super().__init__("[%(asctime)s] %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")


class DetailedFormatter(LogFormatter):
    def __init__(self):
        super().__init__(
            "[%(asctime)s] [%(levelname)s] [%(module)s] [%(thread)d] %(message)s",
            "%Y-%m-%d %H:%M:%S.%f"
        )


class JSONFormatter:
    def __init__(self, time_format: str = "%Y-%m-%dT%H:%M:%S"):
        self.time_format = time_format

    def Format_Message(self, message: LogMessage) -> str:
        import json
        log_dict = {
            "timestamp": message.timestamp,
            "level": message.level.name,
            "level_value": message.level.value,
            "module": message.module_name,
            "message": message.message,
        }
        
        if message.extra_fields:
            log_dict.update(message.extra_fields)
        
        return json.dumps(log_dict, ensure_ascii=False)
